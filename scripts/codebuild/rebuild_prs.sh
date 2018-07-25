payload="{\"repo_url\": \"https://github.com/mrubin-coatue/test/\", \"codebuild_project_name\": \"dummy\", \"buildspec_filename\", \"another_dummy\"}"
aws lambda invoke --function-name testFunction --invocation-type Event --payload $payload lambda_output.txt
