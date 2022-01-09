# glint

## Development instructions
### backend/RESTAPI documentation

[backend/README.md](https://github.com/paulpaul168/glint/tree/main/backend#readme)

### frontend documentation

[frontend/README.md](https://github.com/paulpaul168/glint/tree/main/frontend#readme)

---

## Get started

### First installation
only Fedora and Ubuntu (untested) supported for now

```bash
chmod +x install.sh
./install.sh
```

### Run glint

```bash
./run.sh
```
### Alternativly: run glint via docker
first build the docker container (might need sudo)
```bash
docker build -t glint .
```

spin up docker container (might need sudo)
```bash
docker run -it -p 3000:3000 -p 5000:5000 --rm --name glint-container glint
```

## Milestones

### Milestone 1

- [x] Only Python
- [x] No Projects
- [x] One File
- [x] lint output

### Milestone 2

- [x] File handling (I can edit files and store them to lint the new file)
- [x] File Project handling (frontend: ability to reopen files after closing)
- [x] Jump to source buttons
- [x] Secret Finder UI + basic functionality
- [x] languages: js, go, python

### Milestone 3

- [x] Manual linter selection
- [ ] shareable links
- [ ] Zip file handling (, URL download handling)
- [ ] Docker file
- [ ] Easter eggs
- [x] User defined & stored secret finder regexes
