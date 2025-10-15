# Copyright (c) 2025 Claus Ilginnis
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import re
import typing as t

from flask import Flask, request, session, g
from flask import render_template
from flaskr.db_con import get_db
from flaskr.navigation import Navigation;
from flaskr.forms import FormFields, Form
from mysql.connector import Error as MySQLError

navigation = None

def warning(msg: str):
    session["warnings"].append(msg)
def error(msg: str):
    session["errors"].append(msg)
def info(msg: str):
    session["infos"].append(msg)

def create_app():
    global app
    # create and configure the app
    app = Flask("ToolToucan", instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'   )
        
create_app()

@app.before_request
def before():
    if request.path.startswith('/static/'): # No DB connection for static files
        return
    connection = get_db()
    if connection is None:
        print(f"Database connection failed  for request to {request.path}")
        g.db = None
    else:
        g.db = connection

@app.teardown_request
def teardown(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def render_tt(template: str , **context: t.Any) -> str:
    # Initialize navigation in the session if not present yet
    # This ensures a session-backed navigation per user
    if "errors" not in session:
        session["errors"] = []
    if "infos" not in session:
        session["infos"] = []
    if "warnings" not in session:
        session["warnings"] = []

    n = Navigation()
    n.read(g.db)
        
    result = render_template(
        template,
        navigation=n,     # Pass navigation from session
        errors=session.get("errors", []),     # Optional: pass other session data
        infos=session.get("infos", []),
        warnings=session.get("warnings", []),
        **context
    )
    result = re.sub(r"\n(\s*\n)+", "\n", result)
    result = re.sub("<hr>", "<hr/>", result)
    result = re.sub("<br>", "<br/>", result)
    session["infos"] = []
    session["errors"] = []
    session["warnings"] = []
    return result

# a simple page that says hello
@app.route('/')
def index():
    return render_tt('index.html')

@app.route('/license')
def license():
    return render_tt('license.html')

@app.route('/edit_link/<int:link_id>', methods=['GET'])
def edit_link(link_id):
    cursor=g.db.cursor(dictionary=True)
    cursor.execute("SELECT idLinkCategory,lcName FROM LinkCategory order by idLinkCategory")
    link_categories = cursor.fetchall()
    categories = []
    for row in link_categories:
        categories.append( (row['idLinkCategory'], row['lcName']) )
    
    cursor.close()
    
    cursor=g.db.cursor(dictionary=True)
    cursor.execute("SELECT idHtmlTarget, htText FROM HTMLTarget ORDER BY idHtmlTarget;")
    html_targets_cur = cursor.fetchall()
    html_targets = []
    for row in html_targets_cur:
        html_targets.append( (row['idHtmlTarget'], row['htText']) )
    
    cursor.close()

    form=Form("New Link","/edit_item",None,None)
    form.add_field(FormFields.Hidden("LinkId","idLink",None))
    form.add_field(FormFields.Hidden("action","action","insert"))
    form.add_field(FormFields.Hidden("table","table","Link"))
    form.add_field(FormFields.Hidden("info","info",form.caption))
    form.add_field(FormFields.Hidden("index","index","idLink"))
    form.add_field(FormFields.FixedOptions("Category","lcId",categories,0,True))
    form.add_field(FormFields.Text("Name","lName","",True,45,1,""))
    form.add_field(FormFields.Text("URL","lUri","",True,2048,1,"https?://.+"))
    form.add_field(FormFields.FixedOptions("Target","htId",html_targets,"",True))
    form.add_field(FormFields.Text("Description","lDescription","",False,2048,0,""))
    form.add_field(FormFields.Text("Group","lGroup","",False,100,0,""))

    if link_id is None or link_id==0:
        if "section_id" in request.args:
            section_id=request.args.get("section_id")
            # pre-set section for new link(s)
            form.fields_dict["lcId"].value = int(section_id)
    else:
        # Existing link
        #form=Form("Edit Link","/edit_link","link_id",link_id)
        form.caption = "Edit Link"
        form.new = False
        form.id_name = "idLink"
        form.id_value = link_id
        form.fields_dict["idLink"].value = link_id
        form.fields_dict["action"].value = "update"
        form.fields_dict["info"].value = form.caption
        # Load link data from database and fill the form fields
        cursor=g.db.cursor(dictionary=True)
        cursor.execute(f"""
    SELECT idLink,idLinkCategory,lcName,lGroup,lName,htValue,lUri,lcId,lDescription,htId
    FROM Link JOIN LinkCategory ON Link.lcId = LinkCategory.idLinkCategory
            JOIN HTMLTarget ON Link.htId = HTMLTarget.idHtmlTarget  WHERE idLink = {link_id}
    ORDER BY lcRank , lRank , lcName , lGroup , lName;
    """)
        row=cursor.fetchone()
        if row is None:
            cursor.close()
            error(f"Unknown Link-Id {link_id}")
            return f"Link with ID {link_id} not found.", 404
        form.fields_dict["lName"].value=row["lName"]
        form.fields_dict["lUri"].value=row["lUri"]
        form.fields_dict["lcId"].value=row["lcId"]
        form.fields_dict["lDescription"].value=row["lDescription"]
        form.fields_dict["htId"].value=row["htId"]
        form.fields_dict["lGroup"].value=row["lGroup"]
        cursor.close()
    return render_tt('edit_item.html',form=form)

@app.route('/edit_section/<int:section_id>', methods=['GET'])
def edit_section(section_id):

    form=Form("New Section","/edit_section",None,None)
    form.add_field(FormFields.Hidden("LinkCategory","idLinkCategory",None))
    form.add_field(FormFields.Hidden("action","action","insert"))
    form.add_field(FormFields.Hidden("table","table","LinkCategory"))
    form.add_field(FormFields.Hidden("info","info",form.caption))
    form.add_field(FormFields.Hidden("index","index","idLinkCategory"))
    form.add_field(FormFields.Text("Name","lcName","",True,45,1,""))
    form.add_field(FormFields.Text("Description","lcDescription","",False,2048,0,""))

    if section_id > 0:
        form.caption = "Edit Section"
        form.new = False
        form.id_name = "idLink"
        form.id_value = section_id
        form.fields_dict["idLinkCategory"].value = section_id
        form.fields_dict["action"].value = "update"
        form.fields_dict["info"].value = form.caption
        # Load link data from database and fill the form fields
        cursor=g.db.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM LinkCategory WHERE idLinkCategory = {section_id}")
        row=cursor.fetchone()
        if row is None:
            cursor.close()
            return f"Section with ID {section_id} not found.", 404
        form.fields_dict["lcName"].value=row["lcName"]
        form.fields_dict["lcDescription"].value=row["lcDescription"]

        cursor.close()
    return render_tt('edit_item.html',form=form)

def getAndRemove(d : dict, key: str, default=""):
    if key in d:
        value = d[key]
        del d[key]
        return value
    return default

@app.route('/save_to_db', methods=['POST'])
def save_to_db():
    if request.method != 'POST':
        return render_template('index.html',navigation=navigation)
    form_data = request.form.to_dict(flat=True) # only the first item is of interest
    action= getAndRemove(form_data,"action","") # insert or update
    table= getAndRemove(form_data,"table","") # which table to perform action on
    info_text = getAndRemove(form_data,"info","") # additional info, e.g. id of item to update
    index = getAndRemove(form_data,"index","")
    index_value = getAndRemove(form_data,index,"0")
    fields=[]
    values=[]
    for key, value in form_data.items():
        fields.append(key)
        values.append(value)
    fields_str = ",".join(fields)
    #values_str = ",".join( [f"{v.replace("'","''")}" for v in values] )
    escaped = [str(v).replace("'", "''") for v in values] 
    values_str = ",".join(escaped) 

    cursor=g.db.cursor()
    sql=""
    if action == "insert":
        sql = f"INSERT INTO {table} ({fields_str}) VALUES ({values_str})"
    elif action == "update":
        
        escaped_values = [str(v).replace("'", "''") for v in values]
        updates = ",".join([f"{f}='{ev}'" for f, ev in zip(fields, escaped_values)]) 

        sql = f"UPDATE {table} SET {updates} WHERE {index}={index_value}"
    try:
        cursor.execute(sql)
        g.db.commit()
        info("Saved successfully.")
    except MySQLError as e:
        g.db.rollback()
        error(f"Error saving to database: {e}")
    finally:
        cursor.close()
    return render_tt('index.html')

@app.route('/section_list/<int:section_id>')
def section_list(section_id):
    result_section = None
    navigation = Navigation()
    navigation.read(g.db)
    for section in navigation.sections:
        if section.id == section_id:
            result_section = section
            break
    if result_section is None:
        return f"Section with ID {section_id} not found.", 404
    return render_tt('section_list.html', section=result_section)
