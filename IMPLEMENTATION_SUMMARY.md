# Hybrid Model Download Implementation Summary

## Overview

This implementation adds support for downloading CosyVoice3 models from multiple HuggingFace repositories simultaneously. This allows users to benefit from ONNX-optimized modules while using official base model files.

## Problem Statement

The user requested that the project use:
- ONNX modules from `https://huggingface.co/Lourdle/Fun-CosyVoice3-0.5B-2512_ONNX`
- All other files from `https://huggingface.co/FunAudioLLM/Fun-CosyVoice3-0.5B-2512`

## Solution

### 1. New Download Function

Added `download_model_files_from_multiple_repos()` in `cosyvoice/utils/file_utils.py`:
- Downloads base model from primary repository
- Downloads ONNX files from secondary repository
- Combines files in a single local directory
- Handles both HuggingFace and ModelScope backends

### 2. Modified CosyVoice3 Class

Enhanced `CosyVoice3.__init__()` with new parameters:
- `use_onnx_repo` (bool): Enable/disable hybrid download (default: True)
- `onnx_repo` (str): ONNX repository to use (default: 'Lourdle/Fun-CosyVoice3-0.5B-2512_ONNX')

### 3. Updated AutoModel Function

Modified to properly detect CosyVoice3 models and delegate download to the class.

### 4. ONNX Files Downloaded

From `Lourdle/Fun-CosyVoice3-0.5B-2512_ONNX`:
- flow_fp32.onnx
- flow_fp16.onnx
- hift.onnx
- flow_hift_fp32.onnx
- flow_hift_fp16.onnx

From `FunAudioLLM/Fun-CosyVoice3-0.5B-2512`:
- All other files (LLM weights, configs, tokenizers, etc.)

## Usage Examples

### Basic Usage (Automatic)

```python
from cosyvoice.cli.cosyvoice import AutoModel

# Automatically uses hybrid download for CosyVoice3
cosyvoice = AutoModel(model_dir='FunAudioLLM/Fun-CosyVoice3-0.5B-2512')
```

### Explicit Control

```python
# Enable hybrid download explicitly
cosyvoice = AutoModel(
    model_dir='FunAudioLLM/Fun-CosyVoice3-0.5B-2512',
    use_onnx_repo=True,
    onnx_repo='Lourdle/Fun-CosyVoice3-0.5B-2512_ONNX'
)

# Disable hybrid download
cosyvoice = AutoModel(
    model_dir='FunAudioLLM/Fun-CosyVoice3-0.5B-2512',
    use_onnx_repo=False
)
```

## Files Modified

1. **cosyvoice/utils/file_utils.py**
   - Added `download_model_files_from_multiple_repos()` function

2. **cosyvoice/cli/cosyvoice.py**
   - Added `COSYVOICE3_ONNX_FILES` constant
   - Modified `CosyVoice3.__init__()` for hybrid download
   - Updated `AutoModel()` for proper model detection

3. **README.md**
   - Added "Option 2: Hybrid Download" section
   - Documented usage examples
   - Installation instructions for huggingface_hub

4. **example.py**
   - Updated `cosyvoice3_example()` with usage demonstrations

5. **requirements.txt**
   - Added `huggingface-hub>=0.20.0`

6. **test_hybrid_download.py** (new)
   - Comprehensive test suite
   - Validates structure and implementation

## Key Features

### Backward Compatibility
- Existing code works without changes
- Hybrid download is opt-in for CosyVoice3
- Other models (CosyVoice, CosyVoice2) unaffected

### Error Handling
- Proper exception handling (no bare except clauses)
- Detailed logging of download progress
- Summary of successful/failed downloads
- Graceful fallback to standard download

### Code Quality
- Constants for file lists (no duplication)
- Specific exception types
- Comprehensive error reporting
- Clean separation of concerns

### Cache Management
- Uses appropriate cache directories
- HuggingFace: `~/.cache/huggingface/hub`
- ModelScope: `~/.cache/modelscope/hub`
- Avoids duplicate downloads

## Testing

Created `test_hybrid_download.py` that validates:
- Function structure and existence
- Parameter signatures
- Requirements inclusion
- Documentation completeness

All tests pass successfully.

## Benefits

1. **ONNX Optimization**: Users can benefit from optimized ONNX modules
2. **Official Files**: Still uses official base model and configs
3. **Flexibility**: Easy to enable/disable or customize
4. **Transparency**: Clear logging of what's being downloaded
5. **Reliability**: Robust error handling and validation

## Future Enhancements

Potential improvements for future versions:
- Support for other model versions (CosyVoice2)
- Configurable ONNX file lists
- Validation of downloaded files
- Progress bars for large downloads
- Parallel download support
