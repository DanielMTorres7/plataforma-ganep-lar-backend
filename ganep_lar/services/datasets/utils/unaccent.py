import unicodedata
def unaccent_and_lower(s):
   return (''.join(c for c in unicodedata.normalize('NFKD', s)
                  if unicodedata.category(c) != 'Mn')).lower()