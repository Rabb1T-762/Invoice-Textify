# Invoice-Textify

Welcome to Invoice-Textify! This app allows you to upload images of invoices and process them to extract line-item names, costs, and invoice totals. You can then export this data in convenient formats for further analysis and reporting.

### Currently in development
This app is still in development. 

The current version only supports invoices exactly like the invoices in the testData folder. 
The reason is that the image-to-text areas are currently hard coded and the app can't yet dynamically detect the data and tables. This is a work in progress. 

The app will work with a single file, multiple files, or directories. 

It currently calculates the total of the invoice and adds it to the dictionary under "total" and will output a single excel file with all the data for that invoice. 


## Features

- **Image Upload:** Upload images of invoices for processing.
- **Data Extraction:** Extract line-item names, costs, and invoice totals from uploaded invoices.
- **Export Options:** Export extracted data in convenient formats like text or Excel.

## Getting Started

To get started with Invoice-Textify, you'll need to set up the development environment and run the app locally.

### Prerequisites

- Node.js installed on your machine

### Installation

1. Clone the repository:
https://github.com/Rabb1T-762/Invoice-Textify 

2. Run npm install in the directory

## Contributing

Contributions to Invoice-Texitfy are welcome! If you'd like to contribute, please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bug fix: 
    - Prefix your branch name with "Feature" or "Bug"
3. Commit your changes
4. Push to your repo
5. Submit a pull request

## License
Invoice-Textify is released under the [MIT License](https://opensource.org/licenses/MIT).
