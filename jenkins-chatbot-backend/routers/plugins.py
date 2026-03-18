from fastapi import APIRouter, Query, Request
from fastapi.responses import JSONResponse
from models.schemas import PluginRecommendation, PluginRecommendationResponse
import logging

router = APIRouter()

PLUGIN_DB = [
    PluginRecommendation(
        name="Pipeline",
        description="Jenkins Pipeline plugin for workflow automation.",
        install_command="jenkins-cli install-plugin workflow-aggregator",
        jenkinsfile_snippet="pipeline { agent any; stages { stage('Build') { steps { sh 'make' } } } }"
    ),
    PluginRecommendation(
        name="Git",
        description="Jenkins Git plugin for SCM integration.",
        install_command="jenkins-cli install-plugin git",
        jenkinsfile_snippet="checkout scm"
    ),
    PluginRecommendation(
        name="Docker",
        description="Jenkins Docker plugin for container builds.",
        install_command="jenkins-cli install-plugin docker",
        jenkinsfile_snippet="docker.build('myapp')"
    ),
    PluginRecommendation(
        name="JUnit",
        description="JUnit plugin for test reporting.",
        install_command="jenkins-cli install-plugin junit",
        jenkinsfile_snippet="junit 'results.xml'"
    ),
    PluginRecommendation(
        name="Blue Ocean",
        description="Blue Ocean plugin for modern UI.",
        install_command="jenkins-cli install-plugin blueocean",
        jenkinsfile_snippet="// Blue Ocean UI enabled"
    ),
]

@router.get("/api/plugins/recommend", response_model=PluginRecommendationResponse)
async def recommend_plugins(request: Request, query: str = Query(...)):
    try:
        matched = [p for p in PLUGIN_DB if query.lower() in p.name.lower() or query.lower() in p.description.lower()]
        if not matched:
            matched = PLUGIN_DB[:2]  # fallback
        response = PluginRecommendationResponse(plugins=matched)
        logging.info(f"Plugin recommendation for '{query}': {[p.name for p in matched]}")
        return response
    except Exception as e:
        logging.error(f"Plugin recommendation error: {str(e)}")
        return JSONResponse(status_code=500, content={"plugins": []})
