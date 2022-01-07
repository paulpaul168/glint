# glint

## Get started

### Backend

```bash
sudo apt/dnf install php-cli

cd backend
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
FLASK_APP=glint_server FLASK_ENV=development flask run
```

#### Storage structure:

```
LINT_DIR
|
|____patterns.glint
    |project_name
    |    lint.glint
    |    metadata.glint
    |    file.xy
    |    file2.xy
    |____subfolder
         |   file.xy
         |   file2.yx
```

##### lint.glint:

```json
{
  "status": "done",
  "linters": {
    "language": "{usedLinter}",
    "language2": "{usedLinter}"
  },
  "files": [
    {
      "name": "fileName.py",
      "path": "path/to/file/fileName",
      "linter": "{usedLinter}",
      "lints": [
        {
          "column": 15,
          "endColumn": 35,
          "endLine": 2,
          "header": "Consider using with",
          "line": 1,
          "message": "Using open without explicitly specifying an encoding",
          "url": null
        }
      ]
    }
  ]
}
```

##### metadata.glint:

```json
{
  "name": "projectName"
}
```

##### patterns.glint:

```json
{
  "unique patternID": {
    "patternName": "patternName",
    "regex": "some crazy ass regex"
  }
}
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
- [x] File Project handling (frontend: ability to reopen files after closing)
- [ ] Jump to source buttons & shareable links
- [x] Secret Finder UI + basic functionality
- [x] languages: js, go, python

### Milestone 3

- [ ] Manual linter selection
- [ ] Zip file handling (, URL download handling)
- [ ] Docker file
- [ ] Easter eggs
- [x] User defined & stored secret finder regexes

## RESTful API

---

### POST /api/projects

```json
{
  "name": "projectName",
  "files": [
    {
      "name": "fileName",
      "path": "path/to/file/fileName",
      "content": "{fileContent}"
    }
  ],
  "linters": {
    "language": "linter|auto",
    "language2": "linter|auto"
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
    "language2": "linter|auto"
  }
}
```

fields that should not be updated should be set to `null` (but still specified)
This will automatically start the linting process

Response
http status

```json
{
  "status": "OK"
}
```

### DELETE /api/projects/{projectId}

Response
http status

```json
{
  "status": "OK"
}
```

### GET /api/projects/{projectId}

```json
{
  "name": "projectName",
  "projectId": "projectId",
  "files": [
    {
      "name": "fileName",
      "path": "path/to/file/fileName",
      "content": "{fileContent}"
    }
  ],
  "linters": {
    "language": "linter|auto",
    "language2": "linter|auto"
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
      "lintUrl": "/api/projects/{projectId}/lint"
    }
  ]
}
```

---

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
  "fileUrl": "/api/projects/{projectId}/sources/{fileId}"
}
```

fileId is a string containing the path

### PUT /api/projects/{projectId}/sources/{fileId}

Overwrite existing source file

```json
{
  "path": "{newFilePath}",
  "content": "{fileContent}"
}
```

fileId is a string containing the path
setting a new path also renames the file
fields that should not be updated should be set to `null` (but still specified)

Response
http status

```json
{
  "status": "OK"
}
```

### DELETE /api/projects/{projectId}/sources/{fileId}

Response
http status

```json
{
  "status": "OK"
}
```

---

### GET /api/linters

```json
{
  "language": ["linter1", "linter2"]
}
```

---

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
      "linter": "{usedLinter}",
      "lints": [
        {
          "column": 15,
          "endColumn": 35,
          "endLine": 2,
          "header": "Consider using with",
          "line": 1,
          "message": "Using open without explicitly specifying an encoding",
          "url": null
        }
      ]
    }
  ]
}
```

url, endColumn, endLine and column may be `null`  
Maybe add `"type": "[security|syntax|pretty|...]"` to lints array

If lint is unfinished/errored, response contains:

```json
{
    "status": "processing|{errorMsg}",
    "linters": {
        "language": "linter|auto",
        "language2": "linter|auto",
    }
    "files": []
}
```

if error the http status can be set (500 Internal Server Error || 422 Unprocessable Entity)

### POST /api/searchPatterns

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

### PUT /api/searchPatterns/{patternId}

```json
{
  "patternName": "human readable name",
  "regex": "some crazy ass regex"
}
```

fields that should not be updated should be set to `null` (but still specified)

Response
http status

```json
{
  "status": "OK"
}
```

### DELETE /api/searchPatterns/{patternId}

Response
http status

```json
{
  "status": "OK"
}
```

### GET /api/searchPatterns

```json
{
  "unique patternID": {
    "patternName": "patternName",
    "regex": "some crazy ass regex"
  },
  "unique patternID1": {
    "patternName": "patternName",
    "regex": "some crazy ass regex"
  }
}
```
