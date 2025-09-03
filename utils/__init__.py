from config import PERMIT_DELETE_EXCLUDE_TABLES, EDITABLE_FIELDS
import re


def inject_config():
    return dict(
        EDITABLE_FIELDS=EDITABLE_FIELDS,
        PERMIT_DELETE_EXCLUDE_TABLES=list(PERMIT_DELETE_EXCLUDE_TABLES)
    )


## Unactual for pell??
def protect_user_paragraphs_2DEL(text):
    ## Replace lowcased <p> and </p>, dont touch <P> and </P>
    text = text.replace('<p>', '<P>').replace('</p>', '</P>')
    text = text.replace('<br>', '<BR>')
    return text

## Unactual for pell??
def unprotect_user_paragraphs_2DEL(text):
    ## Retun tags back
    text = text.replace('<P>', '<p>').replace('</P>', '</p>')
    text = text.replace('<BR>', '<br>')
    return text


## Unactual for pell??
def clean_quill_html_2DEL(text):
    if not text:
        return ''
    text = unprotect_user_paragraphs(text)
    return text.strip()
