"""Curriculum audit explorer, conservative initial evidence inventory."""
from pathlib import Path
import csv


def render_audit(st):
    st.header('Curriculum coverage audit · v2.11')
    st.warning('Partial means selected examples exist; it does NOT mean the topic is complete or fully verified.')
    path = Path(__file__).with_name('CURRICULUM_AUDIT.csv')
    with path.open(encoding='utf-8-sig', newline='') as handle:
        rows = list(csv.DictReader(handle))
    subjects = ['All subjects'] + sorted({r['Subject'] for r in rows})
    subject = st.selectbox('Audit subject', subjects, key='audit_subject')
    status = st.selectbox('Coverage filter', ['All topics', 'Partial', 'Not yet verified'], key='audit_status')
    shown = [r for r in rows if (subject == 'All subjects' or r['Subject'] == subject)
             and (status == 'All topics' or r['Status'] == status)]
    st.metric('Topics in selection', len(shown))
    st.dataframe(shown, use_container_width=True, hide_index=True)
    st.caption('Review CURRICULUM_AUDIT.md for the assessment criteria and implementation order.')
