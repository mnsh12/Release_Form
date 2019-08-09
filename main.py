from flask import Flask, request, render_template, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.secret_key = 'xvyual;f;asgnsflejfapzdgksmep'

app.config['MONGO_DBNAME'] = 'mongodb_resources'
app.config['MONGO_URI'] = 'mongodb://Architect:#python9*9@ds257838.mlab.com:57838/mongodb_resources'


mongo = PyMongo(app)


# Application home
@app.route('/home')
@app.route('/')
def index():
    return render_template("index.html")


# Application forms
@app.route('/add/project/new')
def add_new_project():
    return render_template("add_new_project.html")


@app.route('/add/resource/new')
def add_new_resource():
    return render_template("add_new_resource.html")


# Application views
@app.route('/about')
def about():
    return "<h1>(c) 2018, Manish Kamti</h1>"


# Application DB views
@app.route('/view/project/active')
def view_active_projects():
    # get all projects
    all_projects = mongo.db.Projects.find({})

    query_args = request.args
    # redirected while adding a new project
    if len(query_args) != 0:
        # TODO: display the last added project
        # available params
        #  - query_args['project']
        #  - query_args['customer']
        pass

    return render_template("active_projects.html", projects=all_projects)


@app.route('/view/resource/heatmap')
def view_resource_heatmap():
    return render_template("resource_heatmap.html")


@app.route('/view/project/history')
def view_projects_history():
    return render_template("projects_history.html")


@app.route('/test', methods=['GET'])
def test():
    query_args = request.args
    projectName = query_args['projectName']
    return render_template("manage_project.html", projectName=projectName)


@app.route('/view/resource/utilisation')
def view_resource_utilisation():
    # get all resources
    resources = mongo.db.Resources.find({})

    query_args = request.args
    # redirected while adding a new project
    if len(query_args) != 0:
        # TODO: display the last added resource
        # available params
        #  - query_args['resource']
        pass

    return render_template("resource_utilisation.html", resources=resources)


# Application DB additions
@app.route('/add/project', methods=['POST'])
def add_project():
    project = request.get_json()

    projects_collection = mongo.db.Projects
    projects_collection.insert(project)

    response_data = {
        "redirect": True,
        "redirect_url": "/view/project/active?project=" + project['name'] + "&customer=" + project['customer']
    }
    # return render_template("message.html", message="Project details added for: ", object=project)
    return jsonify(response_data)


@app.route('/add/resource', methods=['POST'])
def add_resource():
    resource = request.get_json()

    resources_collection = mongo.db.Resources
    resources_collection.insert(resource)

    # return render_template("message.html", message="Resource details added for: ", object=resource)
    response_data = {
        "redirect": True,
        "redirect_url": "/view/resource/utilisation?resource=" + resource['name']
    }
    return jsonify(response_data)


# Application DB query
@app.route('/query/project', methods=['POST'])
def query_project():
    resource = request.get_json()
    name = resource['projectName']
    jobStage = resource['jobStage']

    project = mongo.db.Projects.find_one({"name": name})

    techList = project["techRequired"]

    # print "Query..."
    # print "Project: ", name
    # print "Job Stage: ", jobStage
    # print "Required technologies: ", techList
    # print "Executing query..."

    query = {}
    query['jobStage'] = jobStage
    query['competence'] = {"$elemMatch": {"technology": {"$in": techList}}}

    resource_cursor = mongo.db.Resources.find(query)
    count = resource_cursor.count()

    resource_list = []

    for resource in resource_cursor:
        name = resource['name']
        signum = resource['signum']
        teamTag = resource['teamTag']
        techComp = []
        for tech in resource['competence']:
            if tech['technology'] in techList:
                t = tech['technology']
                c = tech['competency']
                techComp.append(t+"-"+c)
        resource_list.append({"name": name, "signum": signum, "teamTag": teamTag, "techComp": techComp})

    response_data = {}
    response_data['count'] = count
    response_data['resources'] = resource_list

    return jsonify(response_data)


# Application start
if __name__ == "__main__":
    app.run(debug=True)
