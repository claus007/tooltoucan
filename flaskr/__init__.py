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

from flask import Flask, request
from flask import render_template
from flaskr.db_con import connect_to_database;
from flaskr.navigation import Navigation;
from flaskr.forms import FormFields, Form

navigation = None

def create_app():
    global app
    # create and configure the app
    app = Flask("ToolToucan", instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'   )
    success, error, connection = connect_to_database()
    if success==False:
        print(f"Database connection failed with error: {error}")
        app.config['db_connection'] = None
    else:
        app.config['db_connection'] = connection
        global navigation
        navigation = Navigation().read(connection)
        
create_app()

def render_tt(template: str , **context: t.Any) -> str:
    # ggf. Vorverarbeitung/login
    result = render_template(template, **context)
    result = re.sub(r"\n(\s*\n)+", "\n", result)
    return result

# a simple page that says hello
@app.route('/')
def index():
    return render_tt('index.html',navigation=navigation)

@app.route('/license')
def license():
    return render_tt('license.html',navigation=navigation)

@app.route('/edit_link/<int:link_id>', methods=['GET'])
def edit_link(link_id):
    cursor=app.config['db_connection'].cursor(dictionary=True)
    cursor.execute("SELECT idLinkCategory,lcName FROM LinkCategory order by idLinkCategory")
    link_categories = cursor.fetchall()
    categories = []
    for row in link_categories:
        categories.append( (row['idLinkCategory'], row['lcName']) )
    cursor.close()
    cursor=app.config['db_connection'].cursor(dictionary=True)
    cursor.execute("SELECT dValue, dText FROM HTMLTarget ORDER BY idTarget;")
    html_targets_cur = cursor.fetchall()
    html_targets = []
    for row in html_targets_cur:
        html_targets.append( (row['dValue'], row['dText']) )
    cursor.close()

    form=Form("New Link","/edit_item",None,None)
    form.add_field(FormFields.Hidden("LinkId","idLink",None))
    form.add_field(FormFields.Hidden("action","action","insert"))
    form.add_field(FormFields.Hidden("table","table","Link"))
    form.add_field(FormFields.Hidden("info","info",form.caption))
    form.add_field(FormFields.Hidden("index","index","idLink"))
    form.add_field(FormFields.FixedOptions("Category","lCId",categories,"",True))
    form.add_field(FormFields.Text("Name","lName","",True,45,1,""))
    form.add_field(FormFields.Text("URL","lUri","",True,2048,1,"https?://.+"))
    form.add_field(FormFields.FixedOptions("Target","lDestination",html_targets,"",True))
    form.add_field(FormFields.Text("Description","lDescription","",False,2048,0,""))
    form.add_field(FormFields.Text("Group","lGroup","",False,100,0,""))

    if link_id is None or link_id==0:
        if "section_id" in request.args:
            section_id=request.args.get("section_id")
            # pre-set section for new link(s)
            form.fields_dict["lCId"].value = section_id
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
        cursor=app.config['db_connection'].cursor(dictionary=True)
        cursor.execute(f"""
    SELECT idLink,idLinkCategory,lcName,lGroup,lName,dValue,lUri,lCId,lDescription,dValue,lDestination
    FROM Link JOIN LinkCategory ON Link.lCId = LinkCategory.idLinkCategory
            JOIN HTMLTarget ON Link.lDestination = HTMLTarget.idTarget  WHERE idLink = {link_id}
    ORDER BY lcRank , lRank , lcName , lGroup , lName;
    """)
        row=cursor.fetchone()
        if row is None:
            return f"Link with ID {link_id} not found.", 404
        form.fields_dict["lName"].value=row["lName"]
        form.fields_dict["lUri"].value=row["lUri"]
        form.fields_dict["lCId"].value=row["lCId"]
        form.fields_dict["lDescription"].value=row["lDescription"]
        form.fields_dict["lDestination"].value=row["lDestination"]
        form.fields_dict["lGroup"].value=row["lGroup"]
    return render_tt('edit_item.html',navigation=navigation,form=form)

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
    info = getAndRemove(form_data,"info","") # additional info, e.g. id of item to update
    index = getAndRemove(form_data,"index","")
    index_value = getAndRemove(form_data,index,"0")
    fields=[]
    values=[]
    for key, value in form_data.items():
        fields.append(key)
        values.append(value)
    fields_str = ",".join(fields)
    values_str = ",".join( [f"'{v.replace('\'','\'\'')}'" for v in values] )
    cursor=app.config['db_connection'].cursor()
    sql=""
    if action == "insert":
        sql = f"INSERT INTO {table} ({fields_str}) VALUES ({values_str})"
    elif action == "update":
        sql = f"UPDATE {table} SET " + ",".join( [f"{f}='{v.replace('\'','\'\'')}'" for f,v in zip(fields,values)] ) + f" WHERE {index}={index_value}"
    cursor.execute(sql)
    app.config['db_connection'].commit()
    app.config['db_connection'].close()
    return render_template('index.html',navigation=navigation)

@app.route('/section_list/<int:section_id>')
def edit_section(section_id):
    result_section = None
    for section in navigation.sections:
        if section.id == section_id:
            result_section = section
            break
    if result_section is None:
        return f"Section with ID {section_id} not found.", 404
    return render_tt('section_list.html', navigation=navigation, section=result_section)
