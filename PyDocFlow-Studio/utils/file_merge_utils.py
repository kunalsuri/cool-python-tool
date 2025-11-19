"""
File Merge Utilities Module
Contains core functions for merging text and XML files with metadata.
"""
import os
from datetime import datetime


def generate_text_metadata(file_name, file_path, custom_metadata=""):
    """
    Generate metadata for a text file.
    
    Args:
        file_name: Name of the file
        file_path: Path to the file
        custom_metadata: Custom metadata string
        
    Returns:
        Formatted metadata string
    """
    metadata = f"""
{custom_metadata}
## Data Block Starts
## Metadata Start
## Source Name: {file_name}
## Retrieved Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
## Metadata End

# Data
    """
    return metadata


def generate_xml_metadata(file_name, file_path, custom_metadata=""):
    """
    Generate metadata for an XML file.
    
    Args:
        file_name: Name of the file
        file_path: Path to the file
        custom_metadata: Custom metadata string
        
    Returns:
        Formatted metadata string
    """
    metadata = f"""
{custom_metadata}
<!-- 
## XML Data for file: {file_name}
## Retrieved Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
-->

<!-- ## Beginning of XML Data ## -->
    """
    return metadata


def merge_text_files(folder, output_file, custom_metadata=""):
    """
    Merge all text files in a folder into a single output file with metadata.
    
    Args:
        folder: Input folder path
        output_file: Output file path
        custom_metadata: Custom metadata string
        
    Returns:
        Success message or raises exception
    """
    try:
        files_merged = 0
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for file_name in sorted(os.listdir(folder)):
                file_path = os.path.join(folder, file_name)
                if os.path.isfile(file_path):
                    # Write metadata
                    outfile.write(generate_text_metadata(file_name, file_path, custom_metadata))
                    outfile.write("\n")
                    # Write file content
                    try:
                        with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as infile:
                            outfile.write(infile.read())
                            outfile.write("\n\n### Data Block Ends ###\n")
                            files_merged += 1
                    except Exception as e:
                        outfile.write(f"[Error reading file: {str(e)}]\n\n### Data Block Ends ###\n")
        
        return f"Successfully merged {files_merged} files into {output_file}"
    except Exception as e:
        raise Exception(f"Error merging text files: {str(e)}")


def merge_xml_files(folder, output_file, custom_metadata=""):
    """
    Merge all XML files in a folder into a single output file with metadata.
    
    Args:
        folder: Input folder path
        output_file: Output file path
        custom_metadata: Custom metadata string
        
    Returns:
        Success message or raises exception
    """
    try:
        files_merged = 0
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for file_name in sorted(os.listdir(folder)):
                file_path = os.path.join(folder, file_name)
                if os.path.isfile(file_path) and file_name.endswith('.xml'):
                    # Write metadata
                    outfile.write(generate_xml_metadata(file_name, file_path, custom_metadata))
                    outfile.write("\n")
                    # Write file content
                    try:
                        with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as infile:
                            outfile.write(infile.read())
                            outfile.write("\n\n<!-- ## End of XML Data ## -->\n")
                            files_merged += 1
                    except Exception as e:
                        outfile.write(f"<!-- Error reading file: {str(e)} -->\n<!-- ## End of XML Data ## -->\n")
        
        return f"Successfully merged {files_merged} XML files into {output_file}"
    except Exception as e:
        raise Exception(f"Error merging XML files: {str(e)}")


def merge_files_recursive(input_folder, output_file, custom_metadata=""):
    """
    Merge all files in input folder and subdirectories into output file with metadata.
    
    Args:
        input_folder: Root folder path
        output_file: Output file path
        custom_metadata: Custom metadata string
        
    Returns:
        Success message or raises exception
    """
    try:
        files_merged = 0
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for root, _, files in os.walk(input_folder):
                for file_name in sorted(files):
                    file_path = os.path.join(root, file_name)
                    if os.path.isfile(file_path):
                        # Write metadata
                        relative_path = os.path.relpath(file_path, input_folder)
                        outfile.write(f"\n### START OF EXAMPLE | File: {relative_path} ### \n")
                        outfile.write(f"\n## START OF CODE FOR FILE: {file_name} ##\n\n")

                        # Write file content
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='replace') as infile:
                                outfile.write(infile.read())
                                outfile.write(f"\n\n## END OF CODE ##")
                                outfile.write("\n\n### END OF EXAMPLE ### \n")
                                files_merged += 1
                        except Exception as e:
                            outfile.write(f"[Error reading file: {str(e)}]\n\n## END OF CODE ##\n### END OF EXAMPLE ### \n")
        
        return f"Successfully merged {files_merged} files recursively into {output_file}"
    except Exception as e:
        raise Exception(f"Error merging files recursively: {str(e)}")


def load_default_metadata(file_path="custom-metadata.txt"):
    """
    Load default metadata from file.
    
    Args:
        file_path: Path to metadata file
        
    Returns:
        Default metadata string
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, file_path)

    if os.path.exists(full_path):
        with open(full_path, 'r', encoding='utf-8') as file:
            return file.read()
    else:
        return """# Custom metadata
# Author: Your Name
# Organization: Your Organization
# Date: """ + datetime.now().strftime('%Y-%m-%d')
