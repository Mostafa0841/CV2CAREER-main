import os
import json
from docxtpl import DocxTemplate
import re

def generate_resume_from_json(data, output_folder):
    """
    Generate a resume document from a JSON file and save it in the specified output folder.

    :param json_file: Path to the JSON file containing the resume data.
    :param output_folder: Path to the folder where the generated resume document will be saved.
    """
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)


    # Import the template
    template = DocxTemplate('TOOLS/rt.docx')

    # Render automated report
    template.render(data)

    # Generate filename
    gen_filename = lambda the_string, extension: re.sub('[^0-9a-zA-Z ]+', '', the_string.lower()).replace(' ', '_') + '.' + extension
    docx_file = os.path.join(output_folder, gen_filename(data['Name'], 'docx'))

    # Save the rendered template
    print("Generating resume document: {}".format(docx_file))
    template.save(docx_file)

