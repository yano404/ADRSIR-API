ADRSIR-API
==========

## Requirements
- python >= 3.7
- fastapi >= 0.63.0
- pydantic >= 1.8.1
- SQLAlchemy >= 1.3.23
- uvicorn >= 0.13.4
- smbus >= 1.1

## Usage
Run the app with
```
$ uvicorn adrsir.main:app --host 0.0.0.0
```
and visit `<your raspberry pi IP>:8000/docs/` in your web browser.
You will see the interactive API documentation.

## License
Copyright (c) 2021 Takayuki YANO

The source code is licensed under the MIT License, see LICENSE.
