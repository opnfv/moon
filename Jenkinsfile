properties([
    pipelineTriggers([cron('H * * * *')])
])
node {
    checkout scm
    def packages = ["python_moonutilities","python_moondb","python_moonclient","moon_manager","moon_wrapper","moon_authz","moon_interface","moon_orchestrator"]
    def subtests = [:]
    for (x in packages) {
        def pkg = x
        subtests[pkg] = {
            withDockerContainer('wukongsun/moon_python_unit_test') {
            stage("Install prerequisites for package ${pkg}") {
                sh("pip install pytest requests_mock requests --upgrade")
                    sh("cd ${pkg} && pip install -r tests/unit_python/requirements.txt && pip install .")
                }
                stage("Unit test for package ${pkg}") {
                    sh "cd ${pkg}/tests/unit_python && pytest ."
                }
            }
        }
    }
    parallel subtests
}