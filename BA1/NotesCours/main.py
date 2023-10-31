import os
import tempfile
import shutil

COURSE_NAMES = [
    "AlgebreLineaire",
    "AICC-1",
]
COURSE_NAMES_FORMATTED = {
    "AlgebreLineaire": "Alg\`{e}bre lin\\'{e}aire",
    "AICC-1": "Advanced information, computation, communication I",
}
COURSE_PROGRESS = {
    "AlgebreLineaire": 13,
    "AICC-1": 13,
}


def create_combined_latex(course_name="."):
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as tempdir:
        # List all folders starting with 'Lecture'
        lecture_folders = [
            f
            for f in os.listdir(course_name)
            if os.path.isdir(os.path.join(course_name, f)) and f.startswith("Lecture")
        ]

        # Sort folders by lecture number
        lecture_folders.sort(key=lambda x: int(x.split("Lecture")[1]))

        # Write the combined LaTeX file in the temp directory
        temp_tex_path = os.path.join(tempdir, f"{course_name}.tex")
        with open(temp_tex_path, "w") as out_file:
            # Write the preamble
            out_file.write(
                r"""\documentclass{article}

                \usepackage{./style}

                \title{%s \\[1em] \large R\'{e}sum\'{e} des notes de Joachim Favre}
                \author{Tom Massias Jurien de la Gravi\`{e}re}
                \date{Mercredi 31 octobre 2023}

                \begin{document}
                \maketitle

                \tableofcontents
                \newpage
                """
                % COURSE_NAMES_FORMATTED[course_name]
            )

            # For each lecture folder, input the content of the .tex file
            for folder in lecture_folders[: COURSE_PROGRESS[course_name]]:
                tex_files = [
                    f
                    for f in os.listdir(os.path.join(course_name, folder))
                    if f.endswith(".tex")
                ]
                for tex_file in tex_files:
                    # Copy images to temp directory
                    image_files = [
                        f
                        for f in os.listdir(os.path.join(course_name, folder))
                        if f.endswith((".png", ".jpg", ".jpeg", ".pdf"))
                    ]
                    for image_file in image_files:
                        shutil.copy(
                            os.path.join(course_name, folder, image_file), tempdir
                        )

                    # Skip the preamble and \end{document}
                    skip = False
                    with open(
                        os.path.join(course_name, folder, tex_file), "r"
                    ) as in_file:
                        for line in in_file:
                            if r"\begin{document}" in line:
                                skip = True
                                continue
                            if r"\end{document}" in line:
                                skip = False
                                continue
                            if skip:
                                out_file.write(line)

            # Write the end of the document
            out_file.write(r"\end{document}")

        # Compile the LaTeX file in the temp directory to create the PDF
        for _ in range(2):
            os.system(f"pdflatex -output-directory={tempdir} {temp_tex_path}")

        # Move the PDF from the temp directory to the main directory
        shutil.move(
            os.path.join(tempdir, f"{course_name}.pdf"), f"./outputs/{course_name}.pdf"
        )


if __name__ == "__main__":
    for course_name in COURSE_NAMES:
        create_combined_latex(course_name)
