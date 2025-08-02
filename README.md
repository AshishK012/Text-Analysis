# Web Scraping and Text Analysis
 <h1 style="text-align: center;">Data Extraction and NLP</h1><br>
 <p> This project is designed to automate the extraction and analysis of article content from a list of URLs provided in an Excel file (Input.xlsx). The solution uses web scraping techniques to collect text data and processes it using natural language processing (NLP) techniques such as tokenization and part-of-speech tagging. 
 </p>
<ol>
<li style="font-size: large;"> 
<h3>Data Extraction</h3> 
<p> Input.xlsx <br>
For each of the articles, given in the input.xlsx file, extract the article text and save the extracted article in a text file with URL_ID as its file name.<br>
While extracting text, please make sure your program extracts only the article title and the article text. It should not extract the website header, footer, or anything other than the article text. 
</p><br>
</li>
<li style="font-size: large;">
<h3>Data Anlysis</h3>
<p> For each of the extracted texts from the article, perform textual analysis and compute variables.
            </p><br>
        </li>
<li style="font-size: large;">
<h4>Dependencies and Setup Instructions</h3>
<p> The following Python packages are required:

   - requests
   - pandas
   - nltk
   - re (built-in)
   - os (built-in)
   - bs4 (BeautifulSoup)
   - time (built-in)
   - urllib.parse (built-in)
   
   To install the necessary dependencies, run:

  </p><br>
  </li>

<li style="font-size: large;">
            <h3>Variables</h3>
            <p>
                Definition of each of the variables given in the “Text Analysis.docx” file.<br>
                Look for these variables in the analysis document (Text Analysis.docx):<br>

<ol>
                    <li>POSITIVE SCORE</li>
                    <li>NEGATIVE SCORE</li>
                    <li>POLARITY SCORE</li>
                    <li>SUBJECTIVITY SCORE</li>
                    <li>AVG SENTENCE LENGTH</li>
                    <li>PERCENTAGE OF COMPLEX WORDS</li> 
                    <li>FOG INDEX</li>
                    <li>AVG NUMBER OF WORDS PER SENTENCE</li>
                    <li>COMPLEX WORD COUNT</li>
                    <li>WORD COUNT</li>
                    <li>SYLLABLE PER WORD</li>
                    <li>PERSONAL PRONOUNS</li>
                    <li>AVG WORD LENGTH</li>
                </ol>
            </p>
        </li>
    </ol>
