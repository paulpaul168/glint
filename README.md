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

- [x] Only Python
- [x] No Projects
- [x] One File
- [x] lint output

### Milestone 2

- [x] File handling (I can edit files and store them to lint the new file)
- [ ] File Project handling (frontend: ability to reopen files after closing, jump to source buttons & shareable links)
- [ ] Secret Finder UI + basic functionality
- [ ] languages: js, go, python

### Milestone 3

- [ ] Manual linter selection
- [ ] Zip file handling (, URL download handling)
- [ ] Docker file
- [ ] Easter eggs
- [ ] User defined & stored secret finder regexes

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
            "content": "{fileContent}",
        },
    ],
    "linters": {
        "language": "linter|auto",
        "language2": "linter|auto",
    }
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
```json
{
    "name": "newProjectName",
    "linters": {
        "language": "linter|auto",
        "language2": "linter|auto",
    }
}
```
fields that should not be updated should be set to `null` (but still specified)
This will automatically start the linting process

Response is an echo of the submitted data + http status

### DELETE /api/projects/{projectId}
Response: http status

### GET /api/projects/{projectId}
```json
{
    "name": "projectName",
    "projectId": "projectId",
    "files": [
        {
            "name": "fileName",
            "path": "path/to/file/fileName",
            "content": "{fileContent}",
        },
    ],
    "linters": {
        "language": "linter|auto",
        "language2": "linter|auto",
    }
}
```

### GET /api/projects
Response
```json
{
    "projects": [
        {
            "name": "projectName",
            "projectId": "projectId",
            "projectUrl": "/api/projects/{projectId}",
            "sourcesUrl": "/api/projects/{projectId}/sources",
            "lintUrl": "/api/projects/{projectId}/lint",
        }
    ]
}
```

-----

### POST /api/projects/{projectId}/sources
NEW source file
```json
{
    "fileName": "fileName.ext",
    "path": "path/to/file/fileName",
    "content": "{fileContent}"
}
```

Response
```json
{
    "fileName": "fileName.ext",
    "fileUrl": "/api/projects/{projectId}/sources/{fileId}",
}
```
fileId is a string containing the path

### PUT /api/projects/{projectId}/sources/{fileId}
Overwrite existing source file
```json
{
    "content": "{fileContent}"
}
```
fileId is a string containing the path

Response: http status

### DELETE /api/projects/{projectId}/sources/{fileId}
Response: http status

-----

### GET /api/linters
**Not needed for Milestone 2**
```json
{
    "languages": [
        {
            "language": ["languageName"]
        },
    ]
}
```

-----

### GET /api/projects/{projectId}/lint
Response
```json
{
    "status": "done",
    "linters": {
            "language": "{usedLinter}",
            "language2": "{usedLinter}"
    },
    "files": [
        {
            "name": "fileName",
            "path": "path/to/file/fileName",
            "lints": [
                {
                    "column": 15,
                    "endColumn": 35,
                    "endLine": 2,
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

### POST /api/searchPatterns
**Not needed for Milestone 2**
```json
{
    "patternName": "human readable name",
    "regex": "some crazy ass regex"
}
```

Response
```json
{
    "patternName": "human readable name",
    "patternId": "identifier",
    "regex": "some crazy ass regex"
}
```

### PUT /api/searchPatterns/{secretId}
**Not needed for Milestone 2**
```json
{
    "regex": "some crazy ass regex"
}
```

Response
http status

### GET /api/searchPatterns
**Not needed for Milestone 2**
```json
{
    "searchPatterns": [
        {
            "patternName": "human readable name",
            "patternId": "identifier",
            "regex": "some crazy ass regex"
        }
    ]
}
```
