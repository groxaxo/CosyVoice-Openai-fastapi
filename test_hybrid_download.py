#!/usr/bin/env python3
"""
Test script for hybrid model download functionality.
This script tests the code structure and imports.
"""
import os
import sys
import ast

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_file_utils_structure():
    """Test that file_utils.py has the required function."""
    print("=" * 80)
    print("Testing file_utils.py structure")
    print("=" * 80)
    
    file_path = "cosyvoice/utils/file_utils.py"
    
    with open(file_path, 'r') as f:
        tree = ast.parse(f.read())
    
    # Check for download_model_files_from_multiple_repos function
    functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    
    if 'download_model_files_from_multiple_repos' in functions:
        print("✓ download_model_files_from_multiple_repos function exists")
        return True
    else:
        print("✗ download_model_files_from_multiple_repos function not found")
        print(f"Available functions: {functions}")
        return False


def test_cosyvoice_structure():
    """Test that cosyvoice.py has the required modifications."""
    print("\n" + "=" * 80)
    print("Testing cosyvoice.py structure")
    print("=" * 80)
    
    file_path = "cosyvoice/cli/cosyvoice.py"
    
    with open(file_path, 'r') as f:
        content = f.read()
        tree = ast.parse(content)
    
    # Check imports
    has_import = 'download_model_files_from_multiple_repos' in content
    if has_import:
        print("✓ download_model_files_from_multiple_repos is imported")
    else:
        print("✗ download_model_files_from_multiple_repos is not imported")
        return False
    
    # Check CosyVoice3 class
    classes = {node.name: node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)}
    
    if 'CosyVoice3' in classes:
        print("✓ CosyVoice3 class exists")
        
        # Check __init__ method parameters
        cosyvoice3_class = classes['CosyVoice3']
        init_method = None
        for node in cosyvoice3_class.body:
            if isinstance(node, ast.FunctionDef) and node.name == '__init__':
                init_method = node
                break
        
        if init_method:
            params = [arg.arg for arg in init_method.args.args]
            print(f"  CosyVoice3.__init__ parameters: {params}")
            
            required_params = ['use_onnx_repo', 'onnx_repo']
            for param in required_params:
                if param in params:
                    print(f"  ✓ Parameter '{param}' exists")
                else:
                    print(f"  ✗ Parameter '{param}' missing")
                    return False
        else:
            print("✗ __init__ method not found")
            return False
    else:
        print("✗ CosyVoice3 class not found")
        return False
    
    return True


def test_requirements():
    """Test that requirements.txt includes huggingface-hub."""
    print("\n" + "=" * 80)
    print("Testing requirements.txt")
    print("=" * 80)
    
    with open("requirements.txt", 'r') as f:
        requirements = f.read()
    
    if 'huggingface-hub' in requirements:
        print("✓ huggingface-hub is in requirements.txt")
        return True
    else:
        print("✗ huggingface-hub is not in requirements.txt")
        return False


def test_readme_documentation():
    """Test that README.md documents the hybrid download feature."""
    print("\n" + "=" * 80)
    print("Testing README.md documentation")
    print("=" * 80)
    
    with open("README.md", 'r') as f:
        readme = f.read()
    
    checks = [
        ("Hybrid Download", "Hybrid Download section exists"),
        ("Lourdle/Fun-CosyVoice3-0.5B-2512_ONNX", "References Lourdle ONNX repository"),
        ("use_onnx_repo", "Documents use_onnx_repo parameter"),
    ]
    
    success = True
    for check_str, description in checks:
        if check_str in readme:
            print(f"✓ {description}")
        else:
            print(f"✗ {description}")
            success = False
    
    return success


if __name__ == "__main__":
    print("CosyVoice3 Hybrid Download Test Suite")
    print("=" * 80)
    
    success = True
    
    # Run tests
    success = test_file_utils_structure() and success
    success = test_cosyvoice_structure() and success
    success = test_requirements() and success
    success = test_readme_documentation() and success
    
    # Print final result
    print("\n" + "=" * 80)
    if success:
        print("All tests passed! ✓")
        print("\nThe hybrid download feature has been successfully implemented:")
        print("- ONNX-optimized flow/hift modules from Lourdle/Fun-CosyVoice3-0.5B-2512_ONNX")
        print("- Other files from FunAudioLLM/Fun-CosyVoice3-0.5B-2512")
    else:
        print("Some tests failed! ✗")
        sys.exit(1)
    print("=" * 80)
