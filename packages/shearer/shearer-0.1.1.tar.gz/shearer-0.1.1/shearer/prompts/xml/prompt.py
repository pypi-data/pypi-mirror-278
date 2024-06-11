
PROMPT_PREFIX = """Given the following XML of a {CONTENT_TYPE}. You are asked to extract 
                   the tag that are used to encapsulate the following data:\n
                   {REQUIRED_DATA}\n
                   
                   To successfully extract the required data, you need to examine the content, 
                   find the all the tags, from the outermost tag to the target tags and populate
                   them into a dictionary. For example, if the user is looking for the title of
                   a blog article, then you should look for the tag that encapsulates the title,
                   instead of the site title, or other irrelevant tags that may also be named 
                   as title.

                   An example of site schema output should look like this:
                     ``{{
                          'rss': {{
                            'channel': {{
                                 'author_name': 'target_field',
                                 'item': {{
                                      'title': str,
                                      'link': str,
                                      'description': str,
                                      'pubDate': str
                                 }}
                            }}
                          }}
                     }}``

                   You are asked to generate and return only a python dictionary to store the
                   required information as instructed above, where the key is the tag, and the
                   value MUST BE either a dictionary, or a string "target_field", which
                   represents as the required data as requested by the user. 
                   You should not include other irrelevant object, including string, or answers
                   in your response.
"""
USER_INSTRUCTION = "Here are the content: \n {XML_OBJECT}"
