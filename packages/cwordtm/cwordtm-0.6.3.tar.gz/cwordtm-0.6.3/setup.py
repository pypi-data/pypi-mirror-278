from setuptools import setup, find_packages
from pathlib import Path

this_dir = Path(__file__).parent

VERSION = '0.6.3' 
DESCRIPTION = 'CWordTM: Towards a Topic Modeling Toolkit from Low-Code to Pro-Code'
LONG_DESCRIPTION = (this_dir / "README.rst").read_text()

# Setting up
setup(
        name="cwordtm", 
        version=VERSION,
        author="Dr. Johnny CHENG",
        author_email="<drjohnnycheng@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        project_urls={
            'Documentation': 'https://cwordtm.readthedocs.io',
            'GitHub Repository': 'https://github.com/drjohnnycheng/cwordtm',
        },
        include_package_data=True,
        # packages=find_packages(),
        packages=['cwordtm', 'cwordtm.data', 'cwordtm.dictionary', 'cwordtm.images'],
        # package_dir={"": "."},
        package_data={
            'data': ['*.csv', '*.txt', '*.ttc'],
            'dictionary': ['*.txt'],
            'images': ['*.jpg'],
        },
        install_requires=['numpy', 'pandas', 'importlib_resources', 'regex', 'nltk', \
                    'matplotlib', 'wordcloud', 'pillow', 'jieba', 'gensim', 'pyLDAvis',  \
                    'bertopic',  'transformers', 'spacy', 'seaborn', 'wikipedia', 'scipy', \
                    'importlib', 'networkx', 'plotly', 'IPython', 'scikit-learn', 'torch'],
        
        keywords=['topic modeling', 'BERTopic', 'LDA', 'NMF', 'NLP', 'Holy Bible', \
                  'Chinese text preprocessing', 'pre-packaging', 'low-code', 'pro-code', \
                  'meta programming', 'CWordTM'],

        classifiers= [
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: Information Technology",
            "Intended Audience :: Religion",
            "Intended Audience :: Science/Research",
            "Programming Language :: Python :: 3.10",
            "Operating System :: OS Independent",
        ]
)
