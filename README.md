# 1337 Buster: Decode Leet Speak with Ease (Work in Progress)

        #################################################################
        ##   __ ____ ____ ______   ____            _            
        ##  /_ |___ \___ \____  | |  _ \          | |           
        ##   | | __) |__) |  / /  | |_) |_   _ ___| |_ ___ _ __ 
        ##   | ||__ <|__ <  / /   |  _ <| | | / __| __/ _ \ '__|
        ##   | |___) |__) |/ /    | |_) | |_| \__ \ ||  __/ |   
        ##   |_|____/____//_/     |____/ \__,_|___/\__\___|_|   
        ## 
        #################################################################




1337 Buster is an upcoming NLP library designed to decode leet speak (1337 speak) and convert it back to standard text. It employs a sophisticated three-step process to accurately identify and resolve leet-encoded words.

## How It Works

1337 Buster operates in three main steps:

1. **Identifier**: Uses rule-based logic to detect potential leet candidates within the input text.

2. **Normalizer**: Generates all possible solutions for each identified leet candidate.

3. **Resolver**: Determines the most appropriate solution for each candidate using a combination of NLP techniques:
   - Checks if the proposed solution is a valid word
   - Utilizes a quantized version of FastText (from the compressed-fasttext library) for enhanced accuracy

## Features

- Efficient leet speak decoding
- Rule-based candidate identification
- Multiple solution generation
- Advanced resolution using NLP and compressed FastText
- Easy integration into existing NLP pipelines

## Installation

## Usage

## Contributing

## License
