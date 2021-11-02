# Extract company preference factors

Based on company review data, company preference factors are derived. This project was carried out as a part of the "Unstructured Data Analysis" class at the Department of Data Science, Seoul National University of Science and Technology.
<br></br>

## Deriving preference factors from company review data

In this project, the preference factors of a specific company are derived by using the review data listed on the company review site, among them "Job Planet".

By referring to the rankings and star ratings of companies classified as IT companies on Job Planet, companies ranked 50th or higher were classified as `preferred companies`. In addition, 50 companies with a score of 2 or less were randomly selected and classified as `non-preferred companies`.

LDA, a topic modeling technique, was used to derive corporate preference factors. Preference factors and non-preference factors were derived for preferred and non-preferred companies, respectively.

Recently, the difficulty of finding proper workers is emerging as a serious social problem in Korean society as serious as finding a job. From the company's point of view, it is necessary to identify important factors when selecting a company to recruit talent and prepare for it in advance. This project is expected to be of great help in the preparation process of the company.

A results of this study can be found [here](https://github.com/Kiminjo/Text-analysis-of-papers/files/7459964/3.pdf).

<br></br>

## Dataset

The reviews of workers who have personally worked the company reflect an honest evaluation of the company based on their experiences. Based on anonymity, they can honestly talk about the company's problems that they couldn't even talk about.

The data used in the experiment are as follows.

![data source](https://user-images.githubusercontent.com/42087965/139834244-447270f8-7101-4dad-9c7a-b0b379aaf203.png)

The data was collected from the corporate review site "Job Planet". `Selenium` library was used for data collection.

### Data imblance

When we collected and checked the review data of the target companies, there were twice as many review data of non-preferred companies than that of preferred companies.

So, I went through the process of filtering reviews of non-preferred companies based on the “likes” of the reviews.
<br></br>

## Software Requirements
- python >= 3.5
- selenium
- gensim : A library for natural language processing in Python. It provides various basic topic modeling methods such as LDA, doc2vec, and word2vec.
- konlpy : A library for preprocessing Korean text in Python
- scikit-learn
- numpy 
- pandas 
