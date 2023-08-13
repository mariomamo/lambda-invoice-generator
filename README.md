# lamba-invoice-generator
First of all you have to create the zip package to upload on aws. For that you can use `/docker testing/Dockerfile`.

Go to the root folder and run
```commandline
docker build -t lambda_build "docker testing"
```
And next
```commandline
docker run -v <full_path_to_root_folder>:/code --name lambda_build lambda_build
```