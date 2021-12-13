# glint

## Get started

### Backend

```bash
cd backend
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
FLASK_APP=glint_server FLASK_ENV=development flask run
```

### Frontend

## Milestones

### Milestone 1

- Only Python
- No Projects
- One File
- UI only lint output

## RESTful API

-----

### POST /api/projects
```json
{
    "name": "projectName",
    "files": [
        {
            "name": "fileName",
            "path": "path/to/file/fileName",
            "content": "{fileContent}"
        },
    ],
    "language": "[languageName|default = auto]",
    "linter": "[linterName|default = auto]"
}
```
This will automatically start the linting process

Response
```json
{
    "name": "projectName",
    "projectId": "projectId",
    "projectUrl": "/api/projects/{projectId}",
    "sourcesUrl": "/api/projects/{projectId}/sources",
    "lintUrl": "/api/projects/{projectId}/lint"
}
```
projectName and projectId are "identical", but ID has special characters escaped to be able to store it on a file system

### PATCH /api/projects/{projectId}
**Not needed for Milestone 1**
```json
{
    "name": "newProjectName",
    "language": "newLanguage",
    "linter": "newLinter"
}
```
fields that should not be updated should be set to `null` (but still specified)
This will automatically start the linting process

Response is an echo of the submitted data + http status

### DELETE /api/projects/{projectId}
**Not needed for Milestone 1**
Response: http status

### GET /api/projects
**Not needed for Milestone 1**
Response
```json
{
    "projects": [
        {
            "name": "projectName",
            "projectId": "projectId"
        }
    ]
}
```

-----

### POST /api/projects/{projectId}/sources
**Not needed for Milestone 1**
```json
{
    "name": "fileName",
    "path": "path/to/file/fileName",
    "content": "{fileContent}"
}
```

Response
```json
{
    "name": "fileName",
    "fileUrl": "/api/projects/{projectId}/sources/{fileId}",
}
```
fileId is a string containing the path

### PUT /api/projects/{projectId}/sources/{fileId}
**Not needed for Milestone 1**
```json
{
    "content": "{fileContent}"
}
```
fileId is a string containing the path

Response: http status

### DELETE /api/projects/{projectId}/sources/{fileId}
**Not needed for Milestone 1**
Response: http status

-----

### GET /api/projects/{projectId}/lint
Response
```json
{
    "status": "done",
    "linter": "{usedLinter}",
    "files": [
        {
            "name": "fileName",
            "path": "path/to/file/fileName",
            "lints": [
                {
                    "column": 15,
                    "endColumn": 35,
                    "endline": 2,
                    "header": "Consider using with",
                    "line": 1,
                    "message": "Using open without explicitly specifying an encoding",
                    "url": null,
                }
            ]
        },
    ]
}
```
Maybe add `"type": "[security|syntax|pretty|...]"` to lints array

If lint is unfinished/errored, response contains:
```json
{
    "status": "processing|{errorMsg}",
    "files": []
}
```

if error the http status can be set (500 Internal Server Error || 422 Unprocessable Entity)
**Not needed for Milestone 1**
