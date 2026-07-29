"""Post-install messaging for PyVectorHound"""

def post_install():
    print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ PyVectorHound installed successfully!

📌 WHAT IS THIS?
   Retrieval replay + LLM-powered fixes

🚀 GET STARTED:
   $ python3 -c "from pyvectorhound import *; print('PyVectorHound ready')"
   $ python3 -c "import pyvectorhound; print(f'v{pyvectorhound.__version__ if hasattr(pyvectorhound, \"__version__\") else \"latest\"}')"

📖 DOCUMENTATION:
   Repo:     https://github.com/Mullassery/PyVectorHound
   Tutorials: https://github.com/Mullassery/PyVectorHound#readme
   Issues:    https://github.com/Mullassery/PyVectorHound/issues

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)

if __name__ == "__main__":
    post_install()
