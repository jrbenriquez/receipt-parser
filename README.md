# A fuzzy receipt parser written in Python  

This is a fork of: https://github.com/mre/receipt-parser
[![Build Status](https://travis-ci.org/mre/receipt-parser.svg?branch=master)](https://travis-ci.org/mre/receipt-parser)  
  
Updates

    Added conversion to black and white for better Text Recognition
    Added deskew for better Text Recognition
    Code Updates for changing config files

ToDo

    Modularize (run as modules)
    Use pytesseract or any other python wrapper for tesseract (faster)
    Add training tool
    Easy way of changing config file
    Iterate through the different date formats instead of hardcoding

## Dependencies

* [Tesseract Open Source OCR Engine](https://github.com/tesseract-ocr/tesseract)
* [ImageMagick](http://www.imagemagick.org/script/index.php)

## Usage

To convert all images from the `data/img/` folder to text using tesseract and parse the resulting text files, run

```
make run
```

### Docker

A Dockerfile is available with all dependencies needed to run the program.  
To build the image, run

```
make docker-build
```

To run it on the sample files, try

```
make docker-run
```

By default, running the image will execute the `make run` command. To use with your own images, run the following:

```
docker run -v <path_to_input_images>:/usr/src/app/data/img mre0/receipt-parser
```

## Future Plans

The plan is to write the parsed receipt data into a CSV file. This is enough to create a graph with GnuPlot or any spreadsheet tool. If you want to get fancy, write an output for ElasticSearch and create a nice Kibana dashboard. I'm happy for any pull request.


