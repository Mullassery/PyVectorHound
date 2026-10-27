# Security Vulnerability Audit - pyvectorhound

**Audit Date:** 2026-10-27
**Repository:** /Users/georgimullassery/Desktop/Projects/pyvectorhound
**Total Findings:** 1090

## Summary
- **Critical:** 941
- **High:** 54
- **Medium:** 95

## Findings

### 1. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/PIL/Image.py:3791
- **Description:** eval()
- **Evidence (Line):** `def eval(image: Image, *args: Callable[[int], float]) -> Image:`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 2. [Critical] Hardcoded Secret
- **File:** .venv-test/lib/python3.12/site-packages/PIL/ImageFont.py:1272
- **Description:** AWS Access Key detected
- **Evidence (Line):** `QAHAEwAAQAAAAAAAgAHAGQAAQAAAAAAAwAaAKIAAQAAAAAABAAHAM0AAQAAAAAABQA8AU8AAQAAAA`
- **Exploit Scenario:** Attacker could extract credentials and gain unauthorized access
- **Fix Recommendation:** Move secrets to environment variables or secret manager, rotate compromised credentials
- **Confidence:** High

### 3. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/PIL/ImageMath.py:239
- **Description:** eval()
- **Evidence (Line):** `def lambda_eval(expression: Callable[[dict[str, Any]], Any], **kw: Any) -> Any:`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 4. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/PIL/ImageMath.py:267
- **Description:** eval()
- **Evidence (Line):** `def unsafe_eval(expression: str, **kw: Any) -> Any:`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 5. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/PIL/ImageMath.py:269
- **Description:** eval()
- **Evidence (Line):** `Evaluates an image expression. This uses Python's ``eval()`` function to process`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 6. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/PIL/ImageMath.py:310
- **Description:** eval()
- **Evidence (Line):** `out = builtins.eval(expression, None, args)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 7. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/PIL/ImageShow.py:125
- **Description:** os.system()
- **Evidence (Line):** `os.system(self.get_command(path, **options))  # nosec`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 8. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/_pytest/_code/code.py:164
- **Description:** eval()
- **Evidence (Line):** `def eval(self, code, **vars):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 9. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/_pytest/_code/code.py:173
- **Description:** eval()
- **Evidence (Line):** `return eval(code, self.f_globals, f_locals)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 10. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/_pytest/_code/code.py:326
- **Description:** eval()
- **Evidence (Line):** `# however via `exec(...)` / `eval(...)` they can be other types`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 11. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/_pytest/_code/code.py:326
- **Description:** exec()
- **Evidence (Line):** `# however via `exec(...)` / `eval(...)` they can be other types`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 12. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/_pytest/_py/path.py:1153
- **Description:** exec()
- **Evidence (Line):** `exec(f.read(), mod.__dict__)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 13. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/_pytest/_py/path.py:1159
- **Description:** exec()
- **Evidence (Line):** `def sysexec(self, *argv: os.PathLike[str], **popen_opts: Any) -> str:`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 14. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/_pytest/assertion/rewrite.py:188
- **Description:** exec()
- **Evidence (Line):** `exec(co, module.__dict__)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 15. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/_pytest/assertion/rewrite.py:393
- **Description:** marshal load
- **Evidence (Line):** `co = marshal.load(fp)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 16. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/_pytest/capture.py:1112
- **Description:** os.system()
- **Evidence (Line):** `os.system('echo "hello"')`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 17. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/_pytest/capture.py:1140
- **Description:** os.system()
- **Evidence (Line):** `os.system('echo "hello"')`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 18. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/_pytest/mark/__init__.py:66
- **Description:** eval()
- **Evidence (Line):** `def test_eval(test_input, expected):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 19. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/_pytest/mark/__init__.py:67
- **Description:** eval()
- **Evidence (Line):** `assert eval(test_input) == expected`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 20. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/_pytest/mark/expression.py:295
- **Description:** eval()
- **Evidence (Line):** `"""Adapts a matcher function to a locals mapping as required by eval()."""`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 21. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/_pytest/mark/expression.py:353
- **Description:** eval()
- **Evidence (Line):** `return bool(eval(self._code, {"__builtins__": {}}, MatcherAdapter(matcher)))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 22. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/_pytest/pytester.py:296
- **Description:** eval()
- **Evidence (Line):** `if eval(check, backlocals, call.__dict__):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 23. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/_pytest/skipping.py:92
- **Description:** eval()
- **Evidence (Line):** `If an old-style string condition is given, it is eval()'d, otherwise the`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 24. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/_pytest/skipping.py:119
- **Description:** eval()
- **Evidence (Line):** `result = eval(condition_code, globals_)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 25. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/anyio/_backends/_asyncio.py:2796
- **Description:** exec()
- **Evidence (Line):** `# Use loop.subprocess_shell()/subprocess_exec() rather than their`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 26. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/anyio/_backends/_asyncio.py:2810
- **Description:** exec()
- **Evidence (Line):** `transport, protocol = await loop.subprocess_exec(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 27. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/anyio/to_interpreter.py:123
- **Description:** exec()
- **Evidence (Line):** `exc_info = _interpreters.exec(self._interpreter_id, _run_func)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 28. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/anyio/to_interpreter.py:130
- **Description:** pickle load/dumps
- **Evidence (Line):** `res = pickle.loads(res)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 29. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/anyio/to_process.py:95
- **Description:** pickle load/dumps
- **Evidence (Line):** `retval = pickle.loads(pickled_response)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 30. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/anyio/to_process.py:220
- **Description:** pickle load/dumps
- **Evidence (Line):** `command, *args = pickle.load(stdin.buffer)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 31. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/attr/_make.py:216
- **Description:** eval()
- **Evidence (Line):** `def _compile_and_eval(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 32. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/attr/_make.py:227
- **Description:** eval()
- **Evidence (Line):** `eval(bytecode, globs, locs)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 33. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/attr/_make.py:260
- **Description:** eval()
- **Evidence (Line):** `_compile_and_eval(script, globs, locs, filename)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 34. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/attr/_make.py:1690
- **Description:** eval()
- **Evidence (Line):** `_compile_and_eval(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 35. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/attr/_make.py:1810
- **Description:** eval()
- **Evidence (Line):** `_compile_and_eval(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 36. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/attr/_make.py:1884
- **Description:** eval()
- **Evidence (Line):** `_compile_and_eval(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 37. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/coverage/execfile.py:222
- **Description:** exec()
- **Evidence (Line):** `exec(code, main_mod.__dict__)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 38. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/coverage/execfile.py:335
- **Description:** marshal load
- **Evidence (Line):** `code = marshal.load(fpyc)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 39. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/coverage/htmlfiles/coverage_html.js:236
- **Description:** exec()
- **Evidence (Line):** `const match = /\.([0-9]+)/.exec(cell.textContent);`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 40. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/coverage/parser.py:691
- **Description:** eval()
- **Evidence (Line):** `return True, eval(node.id)  # pylint: disable=eval-used`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 41. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/coverage/templite.py:70
- **Description:** exec()
- **Evidence (Line):** `exec(python_source, global_namespace)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 42. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/datasets/packaged_modules/webdataset/webdataset.py:338
- **Description:** pickle load/dumps
- **Evidence (Line):** `# - "pyd": lambda data: pickle.loads(data)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 43. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/datasets/packaged_modules/webdataset/webdataset.py:339
- **Description:** pickle load/dumps
- **Evidence (Line):** `# - "pickle": lambda data: pickle.loads(data)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 44. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/dill/_dill.py:980
- **Description:** eval()
- **Evidence (Line):** `return eval(repr_str)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 45. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/dill/_dill.py:1038
- **Description:** eval()
- **Evidence (Line):** `return eval(attr+'.__dict__["'+name+'"]')`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 46. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/dill/_dill.py:277
- **Description:** exec()
- **Evidence (Line):** `functions defined via *exec()*.`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 47. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/dill/_dill.py:596
- **Description:** marshal load
- **Evidence (Line):** `return marshal.loads(string)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 48. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/dill/_objects.py:451
- **Description:** shelve usage
- **Evidence (Line):** `# x['DbShelveType'] = shelve.open('foo','n')#,protocol=2) #XXX: delete foo`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 49. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/dill/objtypes.py:18
- **Description:** exec()
- **Evidence (Line):** `exec("%s = type(objects['%s'])" % (_type,_type))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 50. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/dill/source.py:60
- **Description:** eval()
- **Evidence (Line):** `_ = eval("lambda %s : %s" % (lhs,rhs), globals(),locals())`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 51. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/dill/source.py:82
- **Description:** eval()
- **Evidence (Line):** `_f = eval("lambda %s : %s" % (_lhs,_rhs), globals(),locals())`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 52. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/dill/source.py:397
- **Description:** eval()
- **Evidence (Line):** `obj = eval(lines[0].lstrip(name + ' = '))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 53. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/dill/source.py:542
- **Description:** eval()
- **Evidence (Line):** `# _ = eval(getsource(f, force=True)) #XXX: safer but less robust`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 54. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/dill/source.py:178
- **Description:** exec()
- **Evidence (Line):** `#FIXME: all below may fail if exec used (i.e. exec('f = lambda x:x') )`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 55. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/dill/source.py:543
- **Description:** exec()
- **Evidence (Line):** `exec(getimportable(f, alias='_'), __globals__, __locals__)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 56. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/dill/source.py:713
- **Description:** exec()
- **Evidence (Line):** `try: exec(_str) #XXX: check if == obj? (name collision)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 57. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/dill/temp.py:72
- **Description:** eval()
- **Evidence (Line):** `_ = eval("%s" % alias, local)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 58. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/dill/temp.py:221
- **Description:** eval()
- **Evidence (Line):** `_ = eval("%s" % alias, local)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 59. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/dill/temp.py:71
- **Description:** exec()
- **Evidence (Line):** `exec(source, local)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 60. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/dill/temp.py:88
- **Description:** exec()
- **Evidence (Line):** `>>> exec('from %s import f as _f' % modulename)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 61. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/dill/temp.py:220
- **Description:** exec()
- **Evidence (Line):** `exec(source, local)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 62. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/dill/temp.py:133
- **Description:** pickle load/dumps
- **Evidence (Line):** `return pickle.load(open(name, mode=mode, **kwds))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 63. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/dill/temp.py:180
- **Description:** pickle load/dumps
- **Evidence (Line):** `return pickle.load(StringIO(value))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 64. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/dill/tests/test_classdef.py:265
- **Description:** exec()
- **Evidence (Line):** `exec("""class subclass_with_new(metaclass=metaclass_with_new):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 65. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/dill/tests/test_functions.py:33
- **Description:** exec()
- **Evidence (Line):** `exec('''`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 66. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/dill/tests/test_functions.py:104
- **Description:** exec()
- **Evidence (Line):** `exec('''`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 67. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/dill/tests/test_module.py:72
- **Description:** eval()
- **Evidence (Line):** `return eval(str, kwarg, None)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 68. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/dill/tests/test_nested.py:67
- **Description:** pickle load/dumps
- **Evidence (Line):** `la = pickle.loads(pa)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 69. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/dill/tests/test_nested.py:68
- **Description:** pickle load/dumps
- **Evidence (Line):** `lmath = pickle.loads(pmath)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 70. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/dill/tests/test_nested.py:69
- **Description:** pickle load/dumps
- **Evidence (Line):** `lmap = pickle.loads(pmap)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 71. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/dill/tests/test_nested.py:75
- **Description:** pickle load/dumps
- **Evidence (Line):** `_pbasic2 = pickle.loads(pbasic2)()`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 72. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/dill/tests/test_nested.py:77
- **Description:** pickle load/dumps
- **Evidence (Line):** `_pbasic = pickle.loads(pbasic)()`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 73. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/dill/tests/test_nested.py:82
- **Description:** pickle load/dumps
- **Evidence (Line):** `pc2add5 = pickle.loads(pc2adder)(x)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 74. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/dill/tests/test_nested.py:88
- **Description:** pickle load/dumps
- **Evidence (Line):** `pcadd5 = pickle.loads(pcadder)(x)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 75. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/dill/tests/test_nested.py:99
- **Description:** pickle load/dumps
- **Evidence (Line):** `padd5 = pickle.loads(padder)(x)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 76. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/dill/tests/test_nested.py:106
- **Description:** pickle load/dumps
- **Evidence (Line):** `p5add = pickle.loads(pinner)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 77. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/dill/tests/test_objects.py:42
- **Description:** pickle load/dumps
- **Evidence (Line):** `pik = pickle.loads(pickle.dumps(obj))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 78. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/dill/tests/test_sources.py:118
- **Description:** exec()
- **Evidence (Line):** `exec(ds.dumpsource(add, alias='raw'), {}, local)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 79. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/dill/tests/test_sources.py:119
- **Description:** exec()
- **Evidence (Line):** `exec(ds.dumpsource(ts.add, alias='mod'), {}, local)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 80. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/dill/tests/test_sources.py:121
- **Description:** exec()
- **Evidence (Line):** `exec(ds.dumpsource(squared, alias='raw'), {}, local)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 81. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/dill/tests/test_sources.py:122
- **Description:** exec()
- **Evidence (Line):** `exec(ds.dumpsource(ts.squared, alias='mod'), {}, local)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 82. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/dill/tests/test_sources.py:152
- **Description:** exec()
- **Evidence (Line):** `exec(ds.getimport(add, alias='raw'), {}, local)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 83. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/dill/tests/test_sources.py:153
- **Description:** exec()
- **Evidence (Line):** `exec(ds.getimport(ts.add, alias='mod'), {}, local)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 84. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/dill/tests/test_sources.py:155
- **Description:** exec()
- **Evidence (Line):** `exec(ds.getimport(squared, alias='raw'), {}, local)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 85. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/dill/tests/test_sources.py:156
- **Description:** exec()
- **Evidence (Line):** `exec(ds.getimport(ts.squared, alias='mod'), {}, local)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 86. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/dill/tests/test_sources.py:158
- **Description:** exec()
- **Evidence (Line):** `exec(ds.getimport(Bar, alias='raw'), {}, local)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 87. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/dill/tests/test_sources.py:159
- **Description:** exec()
- **Evidence (Line):** `exec(ds.getimport(ts.Bar, alias='mod'), {}, local)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 88. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/dill/tests/test_sources.py:161
- **Description:** exec()
- **Evidence (Line):** `exec(ds.getimport(tm.quad, alias='mod'), {}, local)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 89. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/diskcache/core.py:177
- **Description:** pickle load/dumps
- **Evidence (Line):** `return pickle.load(io.BytesIO(key))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 90. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/diskcache/core.py:282
- **Description:** pickle load/dumps
- **Evidence (Line):** `return pickle.load(reader)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 91. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/diskcache/core.py:284
- **Description:** pickle load/dumps
- **Evidence (Line):** `return pickle.load(io.BytesIO(value))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 92. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/frontmatter/default_handlers.py:260
- **Description:** yaml.load (unsafe)
- **Evidence (Line):** `return yaml.load(fm, **kwargs)  # type: ignore[arg-type]`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 93. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/fsspec/gui.py:312
- **Description:** eval()
- **Evidence (Line):** `return ast.literal_eval(self.kwargs.value) or {}`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 94. [Critical] Hardcoded Secret
- **File:** .venv-test/lib/python3.12/site-packages/fsspec/spec.py:1707
- **Description:** Password Assignment detected
- **Evidence (Line):** `>>> fs = filesystem('ftp', host='test.rebex.net', user='demo', password='password')`
- **Exploit Scenario:** Attacker could extract credentials and gain unauthorized access
- **Fix Recommendation:** Move secrets to environment variables or secret manager, rotate compromised credentials
- **Confidence:** High

### 95. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/fsspec/tests/abstract/mv.py:36
- **Description:** os.system()
- **Evidence (Line):** `os.system(f'icacls "{protected_path}" /deny Everyone:(W)')`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 96. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/fsspec/tests/abstract/mv.py:55
- **Description:** os.system()
- **Evidence (Line):** `os.system(f'icacls "{protected_path}" /remove:d Everyone')`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 97. [Critical] Hardcoded Secret
- **File:** .venv-test/lib/python3.12/site-packages/httpx/_urls.py:336
- **Description:** Password Assignment detected
- **Evidence (Line):** `username="jo@gmail.com", password="a secret"`
- **Exploit Scenario:** Attacker could extract credentials and gain unauthorized access
- **Fix Recommendation:** Move secrets to environment variables or secret manager, rotate compromised credentials
- **Confidence:** High

### 98. [Critical] Hardcoded Secret
- **File:** .venv-test/lib/python3.12/site-packages/httpx2/_urls.py:352
- **Description:** Password Assignment detected
- **Evidence (Line):** `username="jo@gmail.com", password="a secret"`
- **Exploit Scenario:** Attacker could extract credentials and gain unauthorized access
- **Fix Recommendation:** Move secrets to environment variables or secret manager, rotate compromised credentials
- **Confidence:** High

### 99. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/huggingface_hub/cli/extensions.py:223
- **Description:** exec()
- **Evidence (Line):** `def extension_exec(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 100. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/huggingface_hub/cli/sandbox.py:169
- **Description:** exec()
- **Evidence (Line):** `def sandbox_exec(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 101. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/huggingface_hub/hub_mixin.py:695
- **Description:** eval()
- **Evidence (Line):** `is set in evaluation mode by default using `model.eval()` (dropout modules are deactivated). To trai`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 102. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/huggingface_hub/hub_mixin.py:801
- **Description:** eval()
- **Evidence (Line):** `model.eval()  # type: ignore`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 103. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/huggingface_hub/hub_mixin.py:821
- **Description:** eval()
- **Evidence (Line):** `model.eval()  # type: ignore`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 104. [Critical] Hardcoded Secret
- **File:** .venv-test/lib/python3.12/site-packages/huggingface_hub/inference/_client.py:2762
- **Description:** API Key Assignment detected
- **Evidence (Line):** `...     api_key="your-replicate-api-key",  # Pass your Replicate API key directly`
- **Exploit Scenario:** Attacker could extract credentials and gain unauthorized access
- **Fix Recommendation:** Move secrets to environment variables or secret manager, rotate compromised credentials
- **Confidence:** High

### 105. [Critical] Hardcoded Secret
- **File:** .venv-test/lib/python3.12/site-packages/huggingface_hub/inference/_generated/_async_client.py:2810
- **Description:** API Key Assignment detected
- **Evidence (Line):** `...     api_key="your-replicate-api-key",  # Pass your Replicate API key directly`
- **Exploit Scenario:** Attacker could extract credentials and gain unauthorized access
- **Fix Recommendation:** Move secrets to environment variables or secret manager, rotate compromised credentials
- **Confidence:** High

### 106. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/huggingface_hub/utils/tqdm.py:256
- **Description:** exec()
- **Evidence (Line):** `# tracker subprocess via fork_exec(). That path fails when stderr has an invalid`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 107. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/jinja2/bccache.py:73
- **Description:** pickle load/dumps
- **Evidence (Line):** `checksum = pickle.load(f)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 108. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/jinja2/bccache.py:79
- **Description:** marshal load
- **Evidence (Line):** `self.code = marshal.load(f)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 109. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/jinja2/debug.py:145
- **Description:** exec()
- **Evidence (Line):** `exec(code, globals, locals)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 110. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/jinja2/environment.py:1228
- **Description:** exec()
- **Evidence (Line):** `exec(code, namespace)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 111. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/jinja2/lexer.py:663
- **Description:** eval()
- **Evidence (Line):** `value = literal_eval(value_str.replace("_", ""))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 112. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/jinja2/nativetypes.py:40
- **Description:** eval()
- **Evidence (Line):** `return literal_eval(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 113. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/jinja2/nodes.py:581
- **Description:** eval()
- **Evidence (Line):** `representation (objects where ``eval(repr(x)) == x`` is true).`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 114. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/langchain/chains/flare/base.py:135
- **Description:** eval()
- **Evidence (Line):** `def _do_retrieval(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 115. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/langchain/chains/flare/base.py:205
- **Description:** eval()
- **Evidence (Line):** `marginal, finished = self._do_retrieval(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 116. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/langchain_classic/chains/flare/base.py:160
- **Description:** eval()
- **Evidence (Line):** `def _do_retrieval(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 117. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/langchain_classic/chains/flare/base.py:237
- **Description:** eval()
- **Evidence (Line):** `marginal, finished = self._do_retrieval(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 118. [Critical] Hardcoded Secret
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/cache.py:2526
- **Description:** Password Assignment detected
- **Evidence (Line):** `password="password",`
- **Exploit Scenario:** Attacker could extract credentials and gain unauthorized access
- **Fix Recommendation:** Move secrets to environment variables or secret manager, rotate compromised credentials
- **Confidence:** High

### 119. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/callbacks/confident_callback.py:64
- **Description:** eval()
- **Evidence (Line):** `# Import deepeval (not via `import_deepeval` to keep hints in IDEs)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 120. [Critical] Hardcoded Secret
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/chat_message_histories/singlestoredb.py:123
- **Description:** Password Assignment detected
- **Evidence (Line):** `password="password",`
- **Exploit Scenario:** Attacker could extract credentials and gain unauthorized access
- **Fix Recommendation:** Move secrets to environment variables or secret manager, rotate compromised credentials
- **Confidence:** High

### 121. [Critical] Hardcoded Secret
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/chat_models/maritalk.py:58
- **Description:** API Key Assignment detected
- **Evidence (Line):** `chat = ChatMaritalk(api_key="your_api_key_here")`
- **Exploit Scenario:** Attacker could extract credentials and gain unauthorized access
- **Fix Recommendation:** Move secrets to environment variables or secret manager, rotate compromised credentials
- **Confidence:** High

### 122. [Critical] Hardcoded Secret
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/document_loaders/pdf.py:181
- **Description:** Password Assignment detected
- **Evidence (Line):** `password = "my-pasword",`
- **Exploit Scenario:** Attacker could extract credentials and gain unauthorized access
- **Fix Recommendation:** Move secrets to environment variables or secret manager, rotate compromised credentials
- **Confidence:** High

### 123. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/embeddings/ascend.py:46
- **Description:** eval()
- **Evidence (Line):** `self.model = AutoModel.from_pretrained(self.model_path).npu().eval()`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 124. [Critical] Hardcoded Secret
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/embeddings/clova.py:30
- **Description:** API Key Assignment detected
- **Evidence (Line):** `clova_emb_api_key='your_clova_emb_api_key',`
- **Exploit Scenario:** Attacker could extract credentials and gain unauthorized access
- **Fix Recommendation:** Move secrets to environment variables or secret manager, rotate compromised credentials
- **Confidence:** High

### 125. [Critical] Hardcoded Secret
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/embeddings/clova.py:31
- **Description:** API Key Assignment detected
- **Evidence (Line):** `clova_emb_apigw_api_key='your_clova_emb_apigw_api_key',`
- **Exploit Scenario:** Attacker could extract credentials and gain unauthorized access
- **Fix Recommendation:** Move secrets to environment variables or secret manager, rotate compromised credentials
- **Confidence:** High

### 126. [Critical] Hardcoded Secret
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/embeddings/gradient_ai.py:27
- **Description:** Token Assignment detected
- **Evidence (Line):** `gradient_access_token="gradientai-access_token",`
- **Exploit Scenario:** Attacker could extract credentials and gain unauthorized access
- **Fix Recommendation:** Move secrets to environment variables or secret manager, rotate compromised credentials
- **Confidence:** High

### 127. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/embeddings/optimum_intel.py:101
- **Description:** eval()
- **Evidence (Line):** `self.transformer_model.eval()`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 128. [Critical] Hardcoded Secret
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/embeddings/oracleai.py:170
- **Description:** Password Assignment detected
- **Evidence (Line):** `password="<password>",`
- **Exploit Scenario:** Attacker could extract credentials and gain unauthorized access
- **Fix Recommendation:** Move secrets to environment variables or secret manager, rotate compromised credentials
- **Confidence:** High

### 129. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/graphs/hugegraph.py:73
- **Description:** exec()
- **Evidence (Line):** `res = g.exec(query)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 130. [Critical] Hardcoded Secret
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/llms/anyscale.py:75
- **Description:** API Key Assignment detected
- **Evidence (Line):** `anyscalellm = Anyscale(anyscale_api_key="ANYSCALE_API_KEY")`
- **Exploit Scenario:** Attacker could extract credentials and gain unauthorized access
- **Fix Recommendation:** Move secrets to environment variables or secret manager, rotate compromised credentials
- **Confidence:** High

### 131. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/llms/beam.py:216
- **Description:** subprocess with shell=True
- **Evidence (Line):** `process = subprocess.run(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 132. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/llms/databricks.py:243
- **Description:** pickle load/dumps
- **Evidence (Line):** `return cloudpickle.loads(bytes.fromhex(data))  # ignore[pickle]: explicit-opt-in`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 133. [Critical] Hardcoded Secret
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/llms/gradient_ai.py:49
- **Description:** Token Assignment detected
- **Evidence (Line):** `gradient_access_token="gradientai-access_token",`
- **Exploit Scenario:** Attacker could extract credentials and gain unauthorized access
- **Fix Recommendation:** Move secrets to environment variables or secret manager, rotate compromised credentials
- **Confidence:** High

### 134. [Critical] Hardcoded Secret
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/llms/sambanova.py:181
- **Description:** API Key Assignment detected
- **Evidence (Line):** `sambaverse_api_key="your-sambaverse-api-key",`
- **Exploit Scenario:** Attacker could extract credentials and gain unauthorized access
- **Fix Recommendation:** Move secrets to environment variables or secret manager, rotate compromised credentials
- **Confidence:** High

### 135. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/llms/self_hosted.py:40
- **Description:** pickle load/dumps
- **Evidence (Line):** `pipeline = pickle.load(f)  # ignore[pickle]: explicit-opt-in`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 136. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/retrievers/tfidf.py:155
- **Description:** pickle load/dumps
- **Evidence (Line):** `docs, tfidf_array = pickle.load(f)  # ignore[pickle]: explicit-opt-in`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 137. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/tools/riza/command.py:84
- **Description:** exec()
- **Evidence (Line):** `output = self.client.command.exec(language="PYTHON", code=code)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 138. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/tools/riza/command.py:125
- **Description:** exec()
- **Evidence (Line):** `output = self.client.command.exec(language="JAVASCRIPT", code=code)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 139. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/vectorstores/annoy.py:464
- **Description:** pickle load/dumps
- **Evidence (Line):** `) = pickle.load(  # ignore[pickle]: explicit-opt-in`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 140. [Critical] Hardcoded Secret
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/vectorstores/elasticsearch.py:446
- **Description:** Password Assignment detected
- **Evidence (Line):** `es_password="<password>"`
- **Exploit Scenario:** Attacker could extract credentials and gain unauthorized access
- **Fix Recommendation:** Move secrets to environment variables or secret manager, rotate compromised credentials
- **Confidence:** High

### 141. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/vectorstores/faiss.py:1210
- **Description:** pickle load/dumps
- **Evidence (Line):** `) = pickle.load(  # ignore[pickle]: explicit-opt-in`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 142. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/vectorstores/faiss.py:1247
- **Description:** pickle load/dumps
- **Evidence (Line):** `) = pickle.loads(  # ignore[pickle]: explicit-opt-in`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 143. [Critical] Hardcoded Secret
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/vectorstores/neo4j_vector.py:458
- **Description:** Password Assignment detected
- **Evidence (Line):** `password="pleaseletmein"`
- **Exploit Scenario:** Attacker could extract credentials and gain unauthorized access
- **Fix Recommendation:** Move secrets to environment variables or secret manager, rotate compromised credentials
- **Confidence:** High

### 144. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/vectorstores/scann.py:500
- **Description:** pickle load/dumps
- **Evidence (Line):** `) = pickle.load(  # ignore[pickle]: explicit-opt-in`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 145. [Critical] Hardcoded Secret
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/vectorstores/singlestoredb.py:212
- **Description:** Password Assignment detected
- **Evidence (Line):** `password="password",`
- **Exploit Scenario:** Attacker could extract credentials and gain unauthorized access
- **Fix Recommendation:** Move secrets to environment variables or secret manager, rotate compromised credentials
- **Confidence:** High

### 146. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/vectorstores/tiledb.py:191
- **Description:** pickle load/dumps
- **Evidence (Line):** `metadata = pickle.loads(  # ignore[pickle]: explicit-opt-in`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 147. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/langgraph/checkpoint/serde/jsonplus.py:310
- **Description:** pickle load/dumps
- **Evidence (Line):** `return pickle.loads(data_)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 148. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/multiprocess/managers.py:971
- **Description:** exec()
- **Evidence (Line):** `exec('''def %s(self, /, *args, **kwds):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 149. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/multiprocess/sharedctypes.py:153
- **Description:** exec()
- **Evidence (Line):** `exec(template % ((name,)*7), d)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 150. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/multiprocess/spawn.py:130
- **Description:** pickle load/dumps
- **Evidence (Line):** `preparation_data = reduction.pickle.load(from_parent)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 151. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/multiprocess/spawn.py:132
- **Description:** pickle load/dumps
- **Evidence (Line):** `self = reduction.pickle.load(from_parent)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 152. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/multiprocess/tests/__init__.py:4302
- **Description:** pickle load/dumps
- **Evidence (Line):** `sms2 = pickle.loads(pickled_sms)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 153. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/multiprocess/tests/__init__.py:4330
- **Description:** pickle load/dumps
- **Evidence (Line):** `pickle.loads(pickled_sms)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 154. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/multiprocess/tests/__init__.py:4555
- **Description:** pickle load/dumps
- **Evidence (Line):** `deserialized_sl = pickle.loads(serialized_sl)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 155. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/multiprocess/tests/__init__.py:4587
- **Description:** pickle load/dumps
- **Evidence (Line):** `pickle.loads(serialized_sl)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 156. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/multiprocess/util.py:456
- **Description:** exec()
- **Evidence (Line):** `return _posixsubprocess.fork_exec(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 157. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/networkx/algorithms/bipartite/edgelist.py:288
- **Description:** eval()
- **Evidence (Line):** `edgedata = dict(literal_eval(" ".join(d)))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 158. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/networkx/algorithms/bipartite/tests/test_community.py:183
- **Description:** eval()
- **Evidence (Line):** `def _q_merge_delta_via_full_eval(G, C_a, C_b, rest, red, resolution=1, weight="weight"):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 159. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/networkx/algorithms/bipartite/tests/test_community.py:206
- **Description:** eval()
- **Evidence (Line):** `q_delta = _q_merge_delta_via_full_eval(G, {u}, B, [{1, 2, 3}], red)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 160. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/networkx/algorithms/bipartite/tests/test_community.py:219
- **Description:** eval()
- **Evidence (Line):** `q_delta = _q_merge_delta_via_full_eval(G, {u}, B, [{0, 1, 3}], red)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 161. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/networkx/algorithms/bipartite/tests/test_community.py:236
- **Description:** eval()
- **Evidence (Line):** `q_delta = _q_merge_delta_via_full_eval(G, A, B, [], red)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 162. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/networkx/algorithms/bipartite/tests/test_community.py:253
- **Description:** eval()
- **Evidence (Line):** `q_delta = _q_merge_delta_via_full_eval(G, A, B, [], red)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 163. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/networkx/algorithms/bipartite/tests/test_community.py:268
- **Description:** eval()
- **Evidence (Line):** `q_delta = _q_merge_delta_via_full_eval(G, A, B, [], red, resolution=gamma)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 164. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/networkx/algorithms/bipartite/tests/test_community.py:288
- **Description:** eval()
- **Evidence (Line):** `q_delta = _q_merge_delta_via_full_eval(G, A, B, rest, red)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 165. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/networkx/algorithms/bipartite/tests/test_community.py:308
- **Description:** eval()
- **Evidence (Line):** `q_delta = _q_merge_delta_via_full_eval(G, A, B, [], red)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 166. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/networkx/algorithms/flow/tests/test_maxflow_large_graph.py:56
- **Description:** pickle load/dumps
- **Evidence (Line):** `G = pickle.load(f)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 167. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/networkx/algorithms/flow/tests/test_mincost.py:469
- **Description:** pickle load/dumps
- **Evidence (Line):** `G = pickle.load(f)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 168. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/networkx/algorithms/flow/tests/test_networksimplex.py:180
- **Description:** pickle load/dumps
- **Evidence (Line):** `G = pickle.load(f)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 169. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/networkx/algorithms/operators/tests/test_all.py:28
- **Description:** eval()
- **Evidence (Line):** `assert ghj.nodes[n] == eval(graph).nodes[int(node)]`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 170. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/networkx/algorithms/operators/tests/test_binary.py:23
- **Description:** eval()
- **Evidence (Line):** `assert gh.nodes[n] == eval(graph).nodes[int(node)]`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 171. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/networkx/classes/tests/test_coreviews.py:16
- **Description:** pickle load/dumps
- **Evidence (Line):** `pview = pickle.loads(pickle.dumps(view, -1))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 172. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/networkx/classes/tests/test_coreviews.py:19
- **Description:** pickle load/dumps
- **Evidence (Line):** `pview = pickle.loads(pickle.dumps(view))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 173. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/networkx/classes/tests/test_coreviews.py:73
- **Description:** pickle load/dumps
- **Evidence (Line):** `pview = pickle.loads(pickle.dumps(view, -1))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 174. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/networkx/classes/tests/test_coreviews.py:153
- **Description:** pickle load/dumps
- **Evidence (Line):** `pview = pickle.loads(pickle.dumps(view, -1))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 175. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/networkx/classes/tests/test_coreviews.py:211
- **Description:** pickle load/dumps
- **Evidence (Line):** `pview = pickle.loads(pickle.dumps(view, -1))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 176. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/networkx/classes/tests/test_graph.py:268
- **Description:** pickle load/dumps
- **Evidence (Line):** `H = pickle.loads(pickle.dumps(G, -1))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 177. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/networkx/classes/tests/test_graph.py:677
- **Description:** pickle load/dumps
- **Evidence (Line):** `pg = pickle.loads(pickle.dumps(G, -1))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 178. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/networkx/classes/tests/test_graph.py:679
- **Description:** pickle load/dumps
- **Evidence (Line):** `pg = pickle.loads(pickle.dumps(G))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 179. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/networkx/classes/tests/test_graphviews.py:18
- **Description:** pickle load/dumps
- **Evidence (Line):** `prv = pickle.loads(pickle.dumps(rv, -1))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 180. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/networkx/classes/tests/test_graphviews.py:65
- **Description:** pickle load/dumps
- **Evidence (Line):** `prv = pickle.loads(pickle.dumps(rv, -1))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 181. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/networkx/classes/tests/test_graphviews.py:118
- **Description:** pickle load/dumps
- **Evidence (Line):** `pdv = pickle.loads(pickle.dumps(dv, -1))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 182. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/networkx/classes/tests/test_graphviews.py:157
- **Description:** pickle load/dumps
- **Evidence (Line):** `puv = pickle.loads(pickle.dumps(uv, -1))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 183. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/networkx/classes/tests/test_graphviews.py:206
- **Description:** pickle load/dumps
- **Evidence (Line):** `H = pickle.loads(pickle.dumps(G, -1))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 184. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/networkx/classes/tests/test_reportviews.py:22
- **Description:** pickle load/dumps
- **Evidence (Line):** `pnv = pickle.loads(pickle.dumps(nv, -1))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 185. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/networkx/classes/tests/test_reportviews.py:93
- **Description:** pickle load/dumps
- **Evidence (Line):** `pnv = pickle.loads(pickle.dumps(nv, -1))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 186. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/networkx/classes/tests/test_reportviews.py:278
- **Description:** pickle load/dumps
- **Evidence (Line):** `pev = pickle.loads(pickle.dumps(ev, -1))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 187. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/networkx/classes/tests/test_reportviews.py:568
- **Description:** pickle load/dumps
- **Evidence (Line):** `pev = pickle.loads(pickle.dumps(ev, -1))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 188. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/networkx/classes/tests/test_reportviews.py:1027
- **Description:** pickle load/dumps
- **Evidence (Line):** `pdeg = pickle.loads(pickle.dumps(deg, -1))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 189. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/networkx/classes/tests/test_reportviews.py:1416
- **Description:** pickle load/dumps
- **Evidence (Line):** `pickle.loads(pickle.dumps(G, -1))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 190. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/networkx/classes/tests/test_reportviews.py:1427
- **Description:** pickle load/dumps
- **Evidence (Line):** `ev = pickle.loads(pickle.dumps(G.edges, -1))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 191. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/networkx/classes/tests/test_reportviews.py:1430
- **Description:** pickle load/dumps
- **Evidence (Line):** `dv = pickle.loads(pickle.dumps(G.degree, -1))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 192. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/networkx/classes/tests/test_reportviews.py:1434
- **Description:** pickle load/dumps
- **Evidence (Line):** `ev = pickle.loads(pickle.dumps(graph_class([(0, 1), (1, 2)]).edges, -1))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 193. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/networkx/readwrite/edgelist.py:316
- **Description:** eval()
- **Evidence (Line):** `edgedata = dict(literal_eval(edgedata_str.strip()))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 194. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/networkx/readwrite/gml.py:106
- **Description:** eval()
- **Evidence (Line):** `return literal_eval(rep)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 195. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/networkx/readwrite/multiline_adjlist.py:324
- **Description:** eval()
- **Evidence (Line):** `edgedata = literal_eval(data)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 196. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/networkx/readwrite/tests/test_gml.py:454
- **Description:** eval()
- **Evidence (Line):** `data.append(literal_eval("{2.3j, 1 - 2.3j, ()}"))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 197. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/networkx/tests/test_lazy_imports.py:83
- **Description:** exec()
- **Evidence (Line):** `exec(s, {}, locls)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 198. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/networkx/utils/decorators.py:916
- **Description:** exec()
- **Evidence (Line):** `exec(compiled, globl, locl)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 199. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/networkx/utils/tests/test_backends.py:28
- **Description:** pickle load/dumps
- **Evidence (Line):** `assert pickle.loads(pickled) is func.__wrapped__`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 200. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/networkx/utils/tests/test_backends.py:34
- **Description:** pickle load/dumps
- **Evidence (Line):** `assert pickle.loads(pickled) is func`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 201. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/networkx/utils/tests/test_backends.py:37
- **Description:** pickle load/dumps
- **Evidence (Line):** `assert pickle.loads(pickle.dumps(nx.inverse_line_graph)) is nx.inverse_line_graph`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 202. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/networkx/utils/tests/test_config.py:47
- **Description:** pickle load/dumps
- **Evidence (Line):** `cfg2 = pickle.loads(pickle.dumps(cfg))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 203. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/networkx/utils/tests/test_config.py:102
- **Description:** pickle load/dumps
- **Evidence (Line):** `cfg2 = pickle.loads(pickle.dumps(cfg))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 204. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/_internal.py:204
- **Description:** eval()
- **Evidence (Line):** `newitem = (dtype, ast.literal_eval(repeats))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 205. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/arrayprint.py:1577
- **Description:** eval()
- **Evidence (Line):** `>>> assert eval(dtype_short_repr(dt)) == dt`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 206. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/records.py:703
- **Description:** pickle load/dumps
- **Evidence (Line):** `>>> pickle.loads(pickle.dumps(r))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 207. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test__exceptions.py:19
- **Description:** pickle load/dumps
- **Evidence (Line):** `res = pickle.loads(pickle.dumps(error))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 208. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test__exceptions.py:84
- **Description:** pickle load/dumps
- **Evidence (Line):** `exc2 = pickle.loads(pickle.dumps(exc))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 209. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_arrayprint.py:343
- **Description:** eval()
- **Evidence (Line):** `assert_equal(eval(repr(a), vars(np)), a)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 210. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_arrayprint.py:344
- **Description:** eval()
- **Evidence (Line):** `assert_equal(eval(repr(a[0]), {'np': np}), a[0])`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 211. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_custom_dtypes.py:504
- **Description:** pickle load/dumps
- **Evidence (Line):** `res = pickle.loads(s)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 212. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_datetime.py:912
- **Description:** pickle load/dumps
- **Evidence (Line):** `assert_equal(pickle.loads(pickle.dumps(dt, protocol=proto)), dt)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 213. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_datetime.py:914
- **Description:** pickle load/dumps
- **Evidence (Line):** `assert_equal(pickle.loads(pickle.dumps(dt, protocol=proto)), dt)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 214. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_datetime.py:916
- **Description:** pickle load/dumps
- **Evidence (Line):** `assert_equal(pickle.loads(pickle.dumps(scalar, protocol=proto)),`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 215. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_datetime.py:919
- **Description:** pickle load/dumps
- **Evidence (Line):** `assert_equal(pickle.loads(pickle.dumps(delta, protocol=proto)),`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 216. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_datetime.py:926
- **Description:** pickle load/dumps
- **Evidence (Line):** `assert_equal(pickle.loads(pkl), np.dtype('<M8[7D]'))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 217. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_datetime.py:930
- **Description:** pickle load/dumps
- **Evidence (Line):** `assert_equal(pickle.loads(pkl), np.dtype('<M8[W]'))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 218. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_datetime.py:934
- **Description:** pickle load/dumps
- **Evidence (Line):** `assert_equal(pickle.loads(pkl), np.dtype('>M8[us]'))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 219. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_datetime.py:941
- **Description:** pickle load/dumps
- **Evidence (Line):** `res = pickle.loads(pickle.dumps(dt, protocol=proto))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 220. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_dtype.py:996
- **Description:** eval()
- **Evidence (Line):** `assert_equal(np.dtype(eval(str(dt))), dt)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 221. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_dtype.py:1316
- **Description:** pickle load/dumps
- **Evidence (Line):** `pickled = pickle.loads(buf)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 222. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_dtype.py:1387
- **Description:** pickle load/dumps
- **Evidence (Line):** `roundtrip_DType = pickle.loads(pickle.dumps(DType, proto))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 223. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_dtype.py:1398
- **Description:** pickle load/dumps
- **Evidence (Line):** `roundtrip_dt = pickle.loads(pickle.dumps(dt, proto))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 224. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_multiarray.py:1704
- **Description:** eval()
- **Evidence (Line):** `assert_array_equal(eval(repr(xx), {"np": np, "array": np.array}), xx)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 225. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_multiarray.py:4455
- **Description:** eval()
- **Evidence (Line):** `MyType = eval("type('MyType', (base,), class_namespace)",`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 226. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_multiarray.py:11606
- **Description:** exec()
- **Evidence (Line):** `interp.exec("import numpy")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 227. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_multiarray.py:194
- **Description:** pickle load/dumps
- **Evidence (Line):** `vals = pickle.loads(pickle.dumps(a, v))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 228. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_multiarray.py:1856
- **Description:** pickle load/dumps
- **Evidence (Line):** `scalar = pickle.loads(pickle.dumps(scalar))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 229. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_multiarray.py:2008
- **Description:** pickle load/dumps
- **Evidence (Line):** `assert_equal(zs, pickle.loads(zs.dumps()))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 230. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_multiarray.py:2015
- **Description:** pickle load/dumps
- **Evidence (Line):** `zs2 = pickle.loads(p)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 231. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_multiarray.py:2024
- **Description:** pickle load/dumps
- **Evidence (Line):** `pk_load = pickle.loads(pk_dmp)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 232. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_multiarray.py:2035
- **Description:** pickle load/dumps
- **Evidence (Line):** `array_from_buffer = pickle.loads(bytes_string, buffers=buffers)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 233. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_multiarray.py:4953
- **Description:** pickle load/dumps
- **Evidence (Line):** `depickled_arr_with_object = pickle.loads(`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 234. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_multiarray.py:4955
- **Description:** pickle load/dumps
- **Evidence (Line):** `depickled_arr_without_object = pickle.loads(`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 235. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_multiarray.py:4978
- **Description:** pickle load/dumps
- **Evidence (Line):** `depickled_f_contiguous_array = pickle.loads(bytes_string,`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 236. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_multiarray.py:5009
- **Description:** pickle load/dumps
- **Evidence (Line):** `depickled_transposed_contiguous_array = pickle.loads(bytes_string,`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 237. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_multiarray.py:5025
- **Description:** pickle load/dumps
- **Evidence (Line):** `assert_equal(x, pickle.loads(c_contiguous_dumped))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 238. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_multiarray.py:5027
- **Description:** pickle load/dumps
- **Evidence (Line):** `assert_equal(x, pickle.loads(f_contiguous_dumped))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 239. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_multiarray.py:5029
- **Description:** pickle load/dumps
- **Evidence (Line):** `assert_equal(x, pickle.loads(transposed_contiguous_dumped))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 240. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_multiarray.py:5031
- **Description:** pickle load/dumps
- **Evidence (Line):** `assert_equal(x, pickle.loads(no_contiguous_dumped))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 241. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_multiarray.py:5043
- **Description:** pickle load/dumps
- **Evidence (Line):** `depickled_non_contiguous_array = pickle.loads(`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 242. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_multiarray.py:5068
- **Description:** pickle load/dumps
- **Evidence (Line):** `a, pickle.loads(pickle.dumps(a, protocol=proto)),`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 243. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_multiarray.py:5077
- **Description:** pickle load/dumps
- **Evidence (Line):** `return pickle.loads(obj, encoding='latin1')`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 244. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_multiarray.py:5178
- **Description:** pickle load/dumps
- **Evidence (Line):** `new = pickle.loads(pickle.dumps(original_byte_reversed))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 245. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_multiarray.py:9146
- **Description:** pickle load/dumps
- **Evidence (Line):** `res = pickle.loads(pickle_obj)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 246. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_overrides.py:221
- **Description:** pickle load/dumps
- **Evidence (Line):** `roundtripped = pickle.loads(`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 247. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_records.py:184
- **Description:** eval()
- **Evidence (Line):** `recordarr_r = eval("np." + repr(recordarr), {'np': np})`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 248. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_records.py:185
- **Description:** eval()
- **Evidence (Line):** `recarr_r = eval("np." + repr(recarr), {'np': np})`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 249. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_records.py:187
- **Description:** eval()
- **Evidence (Line):** `recordview_r = eval("np." + repr(recordview), {'np': np, 'numpy': np})`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 250. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_records.py:430
- **Description:** pickle load/dumps
- **Evidence (Line):** `assert_equal(a, pickle.loads(pickle.dumps(a, protocol=proto)))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 251. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_records.py:431
- **Description:** pickle load/dumps
- **Evidence (Line):** `assert_equal(a[0], pickle.loads(pickle.dumps(a[0],`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 252. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_records.py:437
- **Description:** pickle load/dumps
- **Evidence (Line):** `assert_equal(a, pickle.loads(pickle.dumps(a, protocol=proto)))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 253. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_records.py:438
- **Description:** pickle load/dumps
- **Evidence (Line):** `assert_equal(a[0], pickle.loads(pickle.dumps(a[0],`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 254. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_records.py:445
- **Description:** pickle load/dumps
- **Evidence (Line):** `pa = pickle.loads(pickle.dumps(a[0], protocol=proto))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 255. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_records.py:469
- **Description:** pickle load/dumps
- **Evidence (Line):** `unpickled = pickle.loads(dump)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 256. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_regression.py:57
- **Description:** pickle load/dumps
- **Evidence (Line):** `b = pickle.load(f)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 257. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_regression.py:369
- **Description:** pickle load/dumps
- **Evidence (Line):** `dt_ = pickle.load(f)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 258. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_regression.py:495
- **Description:** pickle load/dumps
- **Evidence (Line):** `result = pickle.loads(data, encoding='bytes')`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 259. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_regression.py:840
- **Description:** pickle load/dumps
- **Evidence (Line):** `new = pickle.loads(pickle.dumps(el, protocol=proto))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 260. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_regression.py:1076
- **Description:** pickle load/dumps
- **Evidence (Line):** `y = pickle.loads(pickle.dumps(x, protocol=proto))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 261. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_regression.py:1092
- **Description:** pickle load/dumps
- **Evidence (Line):** `xp = pickle.load(f, encoding='latin1')`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 262. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_regression.py:1291
- **Description:** pickle load/dumps
- **Evidence (Line):** `assert_(pickle.loads(`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 263. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_regression.py:1293
- **Description:** pickle load/dumps
- **Evidence (Line):** `assert_(pickle.loads(`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 264. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_regression.py:1899
- **Description:** pickle load/dumps
- **Evidence (Line):** `data = pickle.loads(blob)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 265. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_regression.py:1911
- **Description:** pickle load/dumps
- **Evidence (Line):** `data = pickle.loads(pickle.dumps(data, protocol=proto))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 266. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_regression.py:1932
- **Description:** pickle load/dumps
- **Evidence (Line):** `result = pickle.loads(data, encoding='latin1')`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 267. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_regression.py:1961
- **Description:** pickle load/dumps
- **Evidence (Line):** `result = pickle.loads(data, encoding='latin1')`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 268. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_regression.py:1970
- **Description:** pickle load/dumps
- **Evidence (Line):** `result = pickle.loads(data, encoding='koi8-r')`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 269. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_regression.py:2215
- **Description:** pickle load/dumps
- **Evidence (Line):** `assert_equal(pickle.loads(`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 270. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_regression.py:2435
- **Description:** pickle load/dumps
- **Evidence (Line):** `assert_equal(pickle.loads(dumped), arr)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 271. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_regression.py:2569
- **Description:** pickle load/dumps
- **Evidence (Line):** `result = pickle.loads(test_data, encoding='bytes')`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 272. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_scalarmath.py:610
- **Description:** eval()
- **Evidence (Line):** `#            val2 = eval(val_repr)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 273. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_scalarmath.py:636
- **Description:** eval()
- **Evidence (Line):** `val2 = t(eval(val_repr))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 274. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_simd.py:244
- **Description:** eval()
- **Evidence (Line):** `func = eval(intrin)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 275. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_simd.py:512
- **Description:** eval()
- **Evidence (Line):** `func = eval(intrin[:3])`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 276. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_simd.py:642
- **Description:** eval()
- **Evidence (Line):** `func = eval(intrin)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 277. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_simd.py:703
- **Description:** eval()
- **Evidence (Line):** `npyv_load_tillz, npyv_load_till = eval(intrin)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 278. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_simd.py:723
- **Description:** eval()
- **Evidence (Line):** `npyv_store_till = eval(intrin)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 279. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_simd.py:743
- **Description:** eval()
- **Evidence (Line):** `npyv_loadn = eval(intrin)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 280. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_simd.py:769
- **Description:** eval()
- **Evidence (Line):** `npyv_loadn_tillz, npyv_loadn_till = eval(intrin)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 281. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_simd.py:806
- **Description:** eval()
- **Evidence (Line):** `npyv_storen = eval(intrin)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 282. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_simd.py:845
- **Description:** eval()
- **Evidence (Line):** `npyv_storen_till = eval(intrin)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 283. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_simd.py:897
- **Description:** eval()
- **Evidence (Line):** `intrin = eval(intrin)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 284. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_simd.py:1104
- **Description:** eval()
- **Evidence (Line):** `func = eval(intrin)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 285. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_stringdtype.py:659
- **Description:** pickle load/dumps
- **Evidence (Line):** `res = pickle.load(f)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 286. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_ufunc.py:203
- **Description:** pickle load/dumps
- **Evidence (Line):** `assert_(pickle.loads(pickle.dumps(np.sin,`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 287. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_ufunc.py:208
- **Description:** pickle load/dumps
- **Evidence (Line):** `res = pickle.loads(pickle.dumps(_rational_tests.test_add,`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 288. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_ufunc.py:215
- **Description:** pickle load/dumps
- **Evidence (Line):** `assert_(pickle.loads(astring) is np.cos)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 289. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_ufunc.py:224
- **Description:** pickle load/dumps
- **Evidence (Line):** `obj = pickle.loads(pickle.dumps(_pickleable_module_global.ufunc))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 290. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_ufunc.py:499
- **Description:** pickle load/dumps
- **Evidence (Line):** `int64_2 = pickle.loads(pickle.dumps(int64))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 291. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_umath.py:513
- **Description:** eval()
- **Evidence (Line):** `a, b, divisors = eval(ex_val)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 292. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_umath.py:576
- **Description:** eval()
- **Evidence (Line):** `a = eval(ex_val)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 293. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_umath_accuracy.py:75
- **Description:** eval()
- **Evidence (Line):** `dtype=eval(datatype))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 294. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/_core/tests/test_umath_accuracy.py:78
- **Description:** eval()
- **Evidence (Line):** `dtype=eval(datatype))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 295. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/f2py/auxfuncs.py:632
- **Description:** eval()
- **Evidence (Line):** `return eval(f"{l1}:{' and '.join(l2)}")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 296. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/f2py/auxfuncs.py:640
- **Description:** eval()
- **Evidence (Line):** `return eval(f"{l1}:{' or '.join(l2)}")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 297. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/f2py/auxfuncs.py:644
- **Description:** eval()
- **Evidence (Line):** `return eval('lambda v,f=f:not f(v)')`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 298. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/f2py/capi_maps.py:159
- **Description:** eval()
- **Evidence (Line):** `d = eval(f.read().lower(), {}, {})`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 299. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/f2py/capi_maps.py:299
- **Description:** eval()
- **Evidence (Line):** `ret['size'] = repr(eval(ret['size']))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 300. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/f2py/capi_maps.py:447
- **Description:** eval()
- **Evidence (Line):** `v = eval(v, {}, {})`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 301. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/f2py/crackfortran.py:1325
- **Description:** eval()
- **Evidence (Line):** `v = eval(initexpr, {}, params)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 302. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/f2py/crackfortran.py:2272
- **Description:** eval()
- **Evidence (Line):** `def myeval(e, g=None, l=None):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 303. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/f2py/crackfortran.py:2274
- **Description:** eval()
- **Evidence (Line):** `r = eval(e, g, l)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 304. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/f2py/crackfortran.py:2305
- **Description:** eval()
- **Evidence (Line):** `c = int(myeval(e, {}, {}))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 305. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/f2py/crackfortran.py:2326
- **Description:** eval()
- **Evidence (Line):** `b = myeval(ee, {}, {})`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 306. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/f2py/crackfortran.py:2331
- **Description:** eval()
- **Evidence (Line):** `a = myeval(ee, {}, {}) - b`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 307. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/f2py/crackfortran.py:2336
- **Description:** eval()
- **Evidence (Line):** `c = myeval(ee, {}, {})`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 308. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/f2py/crackfortran.py:2342
- **Description:** eval()
- **Evidence (Line):** `c2 = myeval(ee, {}, {})`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 309. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/f2py/crackfortran.py:2532
- **Description:** eval()
- **Evidence (Line):** `params[n] = param_eval(v, g_params, params, dimspec=dimspec)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 310. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/f2py/crackfortran.py:2562
- **Description:** eval()
- **Evidence (Line):** `value = eval(value, {}, params)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 311. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/f2py/crackfortran.py:2639
- **Description:** eval()
- **Evidence (Line):** `l = str(eval(l, {}, params))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 312. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/f2py/crackfortran.py:2648
- **Description:** eval()
- **Evidence (Line):** `l = str(eval(l, {}, params))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 313. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/f2py/crackfortran.py:2916
- **Description:** eval()
- **Evidence (Line):** `kindselect['kind'] = eval(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 314. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/f2py/crackfortran.py:2966
- **Description:** eval()
- **Evidence (Line):** `def param_eval(v, g_params, params, dimspec=None):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 315. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/f2py/crackfortran.py:2987
- **Description:** eval()
- **Evidence (Line):** `p = eval(v, g_params, params)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 316. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/f2py/crackfortran.py:3018
- **Description:** eval()
- **Evidence (Line):** `item = eval(item, g_params, params)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 317. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/f2py/crackfortran.py:3470
- **Description:** eval()
- **Evidence (Line):** `v = eval(v)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 318. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/f2py/tests/test_crackfortran.py:378
- **Description:** eval()
- **Evidence (Line):** `ret = crackfortran.param_eval(v, g_params, params, dimspec=dimspec)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 319. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/f2py/tests/test_crackfortran.py:388
- **Description:** eval()
- **Evidence (Line):** `ret = crackfortran.param_eval(v, g_params, params, dimspec=dimspec)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 320. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/f2py/tests/test_crackfortran.py:407
- **Description:** eval()
- **Evidence (Line):** `ret = crackfortran.param_eval(v, g_params, params, dimspec=None)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 321. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/f2py/tests/test_f2py2e.py:889
- **Description:** exec()
- **Evidence (Line):** `def test_npd_f77exec():`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 322. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/f2py/tests/test_f2py2e.py:897
- **Description:** exec()
- **Evidence (Line):** `def test_npd_f90exec():`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 323. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/lib/_format_impl.py:536
- **Description:** eval()
- **Evidence (Line):** `See :py:func:`ast.literal_eval()` for details.`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 324. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/lib/_format_impl.py:563
- **Description:** eval()
- **Evidence (Line):** `See :py:func:`ast.literal_eval()` for details.`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 325. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/lib/_format_impl.py:658
- **Description:** eval()
- **Evidence (Line):** `d = ast.literal_eval(header)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 326. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/lib/_format_impl.py:663
- **Description:** eval()
- **Evidence (Line):** `d = ast.literal_eval(header)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 327. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/lib/_format_impl.py:799
- **Description:** eval()
- **Evidence (Line):** `See :py:func:`ast.literal_eval()` for details.`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 328. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/lib/_format_impl.py:929
- **Description:** eval()
- **Evidence (Line):** `See :py:func:`ast.literal_eval()` for details.`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 329. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/lib/_format_impl.py:838
- **Description:** pickle load/dumps
- **Evidence (Line):** `array = pickle.load(fp, **pickle_kwargs)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 330. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/lib/_npyio_impl.py:151
- **Description:** eval()
- **Evidence (Line):** `See :py:func:`ast.literal_eval()` for details.`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 331. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/lib/_npyio_impl.py:356
- **Description:** eval()
- **Evidence (Line):** `See :py:func:`ast.literal_eval()` for details.`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 332. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/lib/_npyio_impl.py:492
- **Description:** pickle load/dumps
- **Evidence (Line):** `"`allow_pickle=` keyword argument or `pickle.load()`.")`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 333. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/lib/_npyio_impl.py:494
- **Description:** pickle load/dumps
- **Evidence (Line):** `return pickle.load(fid, **pickle_kwargs)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 334. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/ma/tests/test_core.py:733
- **Description:** pickle load/dumps
- **Evidence (Line):** `a_pickled = pickle.loads(pickle.dumps(a, protocol=proto))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 335. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/ma/tests/test_core.py:748
- **Description:** pickle load/dumps
- **Evidence (Line):** `a_pickled = pickle.loads(pickle.dumps(a, protocol=proto))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 336. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/ma/tests/test_core.py:757
- **Description:** pickle load/dumps
- **Evidence (Line):** `mc_pickled = pickle.loads(pickle.dumps(mc, protocol=proto))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 337. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/ma/tests/test_core.py:767
- **Description:** pickle load/dumps
- **Evidence (Line):** `a_pickled = pickle.loads(pickle.dumps(a, protocol=proto))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 338. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/ma/tests/test_core.py:776
- **Description:** pickle load/dumps
- **Evidence (Line):** `test = pickle.loads(pickle.dumps(b, protocol=proto))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 339. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/ma/tests/test_core.py:5738
- **Description:** pickle load/dumps
- **Evidence (Line):** `res = pickle.load(f)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 340. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/ma/tests/test_mrecords.py:291
- **Description:** pickle load/dumps
- **Evidence (Line):** `mrec_ = pickle.loads(_)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 341. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/ma/tests/test_old_ma.py:617
- **Description:** pickle load/dumps
- **Evidence (Line):** `y = pickle.loads(s)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 342. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/matrixlib/tests/test_masked_matrix.py:89
- **Description:** pickle load/dumps
- **Evidence (Line):** `a_pickled = pickle.loads(pickle.dumps(a, protocol=proto))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 343. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/polynomial/hermite_e.py:245
- **Description:** eval()
- **Evidence (Line):** `>>> hermeval(0,hermeline(3, 2))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 344. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/polynomial/hermite_e.py:247
- **Description:** eval()
- **Evidence (Line):** `>>> hermeval(1,hermeline(3, 2))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 345. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/polynomial/hermite_e.py:303
- **Description:** eval()
- **Evidence (Line):** `>>> hermeval((-1, 0, 1), coef)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 346. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/polynomial/hermite_e.py:306
- **Description:** eval()
- **Evidence (Line):** `>>> hermeval((-1j, 1j), coef)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 347. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/polynomial/hermite_e.py:790
- **Description:** eval()
- **Evidence (Line):** `tmp[0] += k[i] - hermeval(lbnd, tmp)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 348. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/polynomial/hermite_e.py:796
- **Description:** eval()
- **Evidence (Line):** `def hermeval(x, c, tensor=True):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 349. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/polynomial/hermite_e.py:856
- **Description:** eval()
- **Evidence (Line):** `>>> hermeval(1, coef)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 350. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/polynomial/hermite_e.py:858
- **Description:** eval()
- **Evidence (Line):** `>>> hermeval([[1,2],[3,4]], coef)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 351. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/polynomial/hermite_e.py:1138
- **Description:** eval()
- **Evidence (Line):** ```hermeval(x, c)`` are the same up to roundoff. This equivalence is`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 352. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/polynomial/hermite_e.py:1407
- **Description:** eval()
- **Evidence (Line):** `>>> y = hermeval(x, [1, 2, 3]) + err`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 353. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/polynomial/tests/test_hermite_e.py:79
- **Description:** eval()
- **Evidence (Line):** `val1 = herme.hermeval(self.x, pol1)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 354. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/polynomial/tests/test_hermite_e.py:83
- **Description:** eval()
- **Evidence (Line):** `val2 = herme.hermeval(self.x, pol2)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 355. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/polynomial/tests/test_hermite_e.py:85
- **Description:** eval()
- **Evidence (Line):** `val3 = herme.hermeval(self.x, pol3)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 356. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/polynomial/tests/test_hermite_e.py:120
- **Description:** eval()
- **Evidence (Line):** `def test_hermeval(self):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 357. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/polynomial/tests/test_hermite_e.py:122
- **Description:** eval()
- **Evidence (Line):** `assert_equal(herme.hermeval([], [1]).size, 0)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 358. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/polynomial/tests/test_hermite_e.py:130
- **Description:** eval()
- **Evidence (Line):** `res = herme.hermeval(x, [0] * i + [1])`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 359. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/polynomial/tests/test_hermite_e.py:137
- **Description:** eval()
- **Evidence (Line):** `assert_equal(herme.hermeval(x, [1]).shape, dims)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 360. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/polynomial/tests/test_hermite_e.py:138
- **Description:** eval()
- **Evidence (Line):** `assert_equal(herme.hermeval(x, [1, 0]).shape, dims)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 361. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/polynomial/tests/test_hermite_e.py:139
- **Description:** eval()
- **Evidence (Line):** `assert_equal(herme.hermeval(x, [1, 0, 0]).shape, dims)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 362. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/polynomial/tests/test_hermite_e.py:258
- **Description:** eval()
- **Evidence (Line):** `assert_almost_equal(herme.hermeval(-1, hermeint), i)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 363. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/polynomial/tests/test_hermite_e.py:379
- **Description:** eval()
- **Evidence (Line):** `assert_almost_equal(v[..., i], herme.hermeval(x, coef))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 364. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/polynomial/tests/test_hermite_e.py:387
- **Description:** eval()
- **Evidence (Line):** `assert_almost_equal(v[..., i], herme.hermeval(x, coef))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 365. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/polynomial/tests/test_hermite_e.py:444
- **Description:** eval()
- **Evidence (Line):** `assert_almost_equal(herme.hermeval(x, coef3), y)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 366. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/polynomial/tests/test_hermite_e.py:447
- **Description:** eval()
- **Evidence (Line):** `assert_almost_equal(herme.hermeval(x, coef3), y)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 367. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/polynomial/tests/test_hermite_e.py:451
- **Description:** eval()
- **Evidence (Line):** `assert_almost_equal(herme.hermeval(x, coef4), y)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 368. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/polynomial/tests/test_hermite_e.py:454
- **Description:** eval()
- **Evidence (Line):** `assert_almost_equal(herme.hermeval(x, coef4), y)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 369. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/polynomial/tests/test_hermite_e.py:458
- **Description:** eval()
- **Evidence (Line):** `assert_almost_equal(herme.hermeval(x, coef4), y)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 370. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/polynomial/tests/test_hermite_e.py:487
- **Description:** eval()
- **Evidence (Line):** `assert_almost_equal(herme.hermeval(x, coef1), y)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 371. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/polynomial/tests/test_hermite_e.py:489
- **Description:** eval()
- **Evidence (Line):** `assert_almost_equal(herme.hermeval(x, coef2), y)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 372. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/polynomial/tests/test_hermite_e.py:535
- **Description:** eval()
- **Evidence (Line):** `res = herme.hermeval(roots, pol)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 373. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/polynomial/tests/test_polynomial.py:62
- **Description:** pickle load/dumps
- **Evidence (Line):** `y = pickle.loads(pickle.dumps(x))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 374. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/random/tests/test_direct.py:328
- **Description:** pickle load/dumps
- **Evidence (Line):** `reloaded = pickle.loads(bitgen_pkl)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 375. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/random/tests/test_direct.py:336
- **Description:** pickle load/dumps
- **Evidence (Line):** `aa = pickle.loads(pickle.dumps(ss))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 376. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/random/tests/test_direct.py:346
- **Description:** pickle load/dumps
- **Evidence (Line):** `bg_plk = pickle.loads(pickle.dumps(bit_generator))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 377. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/random/tests/test_direct.py:352
- **Description:** pickle load/dumps
- **Evidence (Line):** `bg_plk = pickle.loads(pickle.dumps(bit_generator))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 378. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/random/tests/test_direct.py:580
- **Description:** pickle load/dumps
- **Evidence (Line):** `sfc = pickle.load(gz)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 379. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/random/tests/test_generator_mt19937.py:2802
- **Description:** pickle load/dumps
- **Evidence (Line):** `rg_plk = pickle.loads(pickle.dumps(rg))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 380. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/random/tests/test_generator_mt19937.py:2808
- **Description:** pickle load/dumps
- **Evidence (Line):** `rg_plk = pickle.loads(pickle.dumps(rg))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 381. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/random/tests/test_generator_mt19937.py:2824
- **Description:** pickle load/dumps
- **Evidence (Line):** `rg = pickle.load(gz)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 382. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/random/tests/test_randomstate.py:272
- **Description:** pickle load/dumps
- **Evidence (Line):** `rs_unpick = pickle.loads(pickle.dumps(random_state))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 383. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/random/tests/test_smoke.py:488
- **Description:** pickle load/dumps
- **Evidence (Line):** `unpick = pickle.loads(pick)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 384. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/random/tests/test_smoke.py:494
- **Description:** pickle load/dumps
- **Evidence (Line):** `unpick = pickle.loads(pick)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 385. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/testing/_private/utils.py:1352
- **Description:** exec()
- **Evidence (Line):** `exec(astr, dict)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 386. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/testing/_private/utils.py:1640
- **Description:** exec()
- **Evidence (Line):** `exec(code, globs, locs)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 387. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/numpy/tests/test_public_api.py:322
- **Description:** eval()
- **Evidence (Line):** `eval(module_name)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 388. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/numpy/tests/test_reloading.py:40
- **Description:** pickle load/dumps
- **Evidence (Line):** `assert_(pickle.loads(pickle.dumps(np._NoValue,`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 389. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/packaging/_parser.py:332
- **Description:** eval()
- **Evidence (Line):** `value = ast.literal_eval(python_str)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 390. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/packaging/licenses/__init__.py:100
- **Description:** eval()
- **Evidence (Line):** `invalid = eval(python_expression, globals(), locals())`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 391. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/core/computation/eval.py:179
- **Description:** eval()
- **Evidence (Line):** `def eval(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 392. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/core/computation/eval.py:328
- **Description:** eval()
- **Evidence (Line):** `>>> pd.eval("double_age = df.age * 2", target=df)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 393. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/core/computation/expr.py:489
- **Description:** eval()
- **Evidence (Line):** `def _maybe_eval(self, binop, eval_in_python):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 394. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/core/computation/expr.py:523
- **Description:** eval()
- **Evidence (Line):** `return self._maybe_eval(res, self.binary_ops)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 395. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/core/computation/expr.py:527
- **Description:** eval()
- **Evidence (Line):** `return self._maybe_eval(res, eval_in_python)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 396. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/core/computation/expr.py:537
- **Description:** eval()
- **Evidence (Line):** `return self._maybe_eval(res, eval_in_python + maybe_eval_in_python)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 397. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/core/computation/expr.py:584
- **Description:** eval()
- **Evidence (Line):** `result = pd_eval(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 398. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/core/computation/expr.py:592
- **Description:** eval()
- **Evidence (Line):** `lhs = pd_eval(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 399. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/core/computation/ops.py:425
- **Description:** eval()
- **Evidence (Line):** `res = eval(self, local_dict=env, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 400. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/core/computation/scope.py:200
- **Description:** eval()
- **Evidence (Line):** ```DataFrame.eval()`` and ``DataFrame.query()``.`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 401. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/core/frame.py:5195
- **Description:** eval()
- **Evidence (Line):** `res = self.eval(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 402. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/core/frame.py:5220
- **Description:** eval()
- **Evidence (Line):** `def eval(self, expr: str, *, inplace: Literal[False] = ..., **kwargs) -> Any: ...`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 403. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/core/frame.py:5223
- **Description:** eval()
- **Evidence (Line):** `def eval(self, expr: str, *, inplace: Literal[True], **kwargs) -> None: ...`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 404. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/core/frame.py:5225
- **Description:** eval()
- **Evidence (Line):** `def eval(self, expr: str, *, inplace: bool = False, **kwargs) -> Any | None:`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 405. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/core/frame.py:5300
- **Description:** eval()
- **Evidence (Line):** `>>> df.eval("A + B")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 406. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/core/frame.py:5311
- **Description:** eval()
- **Evidence (Line):** `>>> df.eval("D = A + B")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 407. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/core/frame.py:5328
- **Description:** eval()
- **Evidence (Line):** `>>> df.eval(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 408. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/core/frame.py:5344
- **Description:** eval()
- **Evidence (Line):** `>>> df.eval("B * `C&C`")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 409. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/core/frame.py:5356
- **Description:** eval()
- **Evidence (Line):** `>>> df.eval("@local_var * A")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 410. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/core/frame.py:5375
- **Description:** eval()
- **Evidence (Line):** `return _eval(expr, inplace=inplace, **kwargs)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 411. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/errors/__init__.py:713
- **Description:** eval()
- **Evidence (Line):** `>>> pd.eval("sin + a", engine="numexpr")  # doctest: +SKIP`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 412. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/errors/__init__.py:745
- **Description:** eval()
- **Evidence (Line):** `>>> pd.eval("x + 1")  # doctest: +SKIP`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 413. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/pandas/io/pickle.py:233
- **Description:** pickle load/dumps
- **Evidence (Line):** `return pickle.load(handles.handle)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 414. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/arrays/string_/test_string_arrow.py:259
- **Description:** pickle load/dumps
- **Evidence (Line):** `result = pickle.loads(full_pickled)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 415. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/arrays/string_/test_string_arrow.py:262
- **Description:** pickle load/dumps
- **Evidence (Line):** `result_sliced = pickle.loads(sliced_pickled)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 416. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_compat.py:31
- **Description:** eval()
- **Evidence (Line):** `res = pd.eval("a + b", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 417. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:156
- **Description:** eval()
- **Evidence (Line):** `pd.eval(ex, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 418. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:164
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval(ex, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 419. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:176
- **Description:** eval()
- **Evidence (Line):** `pd.eval(ex, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 420. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:190
- **Description:** eval()
- **Evidence (Line):** `pd.eval(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 421. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:198
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval(ex, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 422. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:207
- **Description:** eval()
- **Evidence (Line):** `pd.eval(ex, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 423. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:235
- **Description:** eval()
- **Evidence (Line):** `pd.eval(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 424. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:250
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval(ex, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 425. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:261
- **Description:** eval()
- **Evidence (Line):** `pd.eval(ex1, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 426. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:274
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval(ex, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 427. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:283
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval(ex, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 428. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:288
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval(ex, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 429. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:308
- **Description:** eval()
- **Evidence (Line):** `expected = eval(f"nlhs {arith1} ghs")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 430. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:315
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval(ex, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 431. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:337
- **Description:** eval()
- **Evidence (Line):** `res = pd.eval(ex, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 432. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:346
- **Description:** eval()
- **Evidence (Line):** `pd.eval(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 433. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:358
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval(ex, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 434. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:373
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval(ex, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 435. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:386
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval("~elb", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 436. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:399
- **Description:** eval()
- **Evidence (Line):** `pd.eval(expr, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 437. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:403
- **Description:** eval()
- **Evidence (Line):** `pd.eval(expr, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 438. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:410
- **Description:** eval()
- **Evidence (Line):** `pd.eval(expr, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 439. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:413
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval(expr, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 440. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:419
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval(expr, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 441. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:428
- **Description:** eval()
- **Evidence (Line):** `pd.eval(expr, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 442. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:432
- **Description:** eval()
- **Evidence (Line):** `pd.eval(expr, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 443. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:444
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval(expr, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 444. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:448
- **Description:** eval()
- **Evidence (Line):** `pd.eval(expr, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 445. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:455
- **Description:** eval()
- **Evidence (Line):** `pd.eval(expr, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 446. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:458
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval(expr, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 447. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:464
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval(expr, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 448. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:475
- **Description:** eval()
- **Evidence (Line):** `pd.eval(expr, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 449. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:479
- **Description:** eval()
- **Evidence (Line):** `pd.eval(expr, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 450. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:487
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval(expr, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 451. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:493
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval(expr, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 452. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:501
- **Description:** eval()
- **Evidence (Line):** `pd.eval(expr, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 453. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:504
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval(expr, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 454. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:513
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval(expr, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 455. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:519
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval(expr, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 456. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:527
- **Description:** eval()
- **Evidence (Line):** `pd.eval(expr, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 457. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:530
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval(expr, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 458. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:549
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval(expr, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 459. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:568
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval(expr, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 460. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:579
- **Description:** eval()
- **Evidence (Line):** `pd.eval("~1.0", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 461. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:581
- **Description:** eval()
- **Evidence (Line):** `assert pd.eval("-1.0", parser=parser, engine=engine) == -1.0`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 462. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:582
- **Description:** eval()
- **Evidence (Line):** `assert pd.eval("+1.0", parser=parser, engine=engine) == +1.0`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 463. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:583
- **Description:** eval()
- **Evidence (Line):** `assert pd.eval("~1", parser=parser, engine=engine) == ~1`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 464. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:584
- **Description:** eval()
- **Evidence (Line):** `assert pd.eval("-1", parser=parser, engine=engine) == -1`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 465. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:585
- **Description:** eval()
- **Evidence (Line):** `assert pd.eval("+1", parser=parser, engine=engine) == +1`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 466. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:589
- **Description:** eval()
- **Evidence (Line):** `assert pd.eval("~True", parser=parser, engine=engine) == ~True`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 467. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:593
- **Description:** eval()
- **Evidence (Line):** `assert pd.eval("~False", parser=parser, engine=engine) == ~False`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 468. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:594
- **Description:** eval()
- **Evidence (Line):** `assert pd.eval("-True", parser=parser, engine=engine) == -True`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 469. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:595
- **Description:** eval()
- **Evidence (Line):** `assert pd.eval("-False", parser=parser, engine=engine) == -False`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 470. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:596
- **Description:** eval()
- **Evidence (Line):** `assert pd.eval("+True", parser=parser, engine=engine) == +True`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 471. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:597
- **Description:** eval()
- **Evidence (Line):** `assert pd.eval("+False", parser=parser, engine=engine) == +False`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 472. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:604
- **Description:** eval()
- **Evidence (Line):** `pd.eval("[-True, True, +True, -False, False, +False, -37, 37, ~37, +37]"),`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 473. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:628
- **Description:** eval()
- **Evidence (Line):** `res = df.eval(expr)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 474. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:635
- **Description:** eval()
- **Evidence (Line):** `result = df.eval("x.fillna(-1)")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 475. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:641
- **Description:** eval()
- **Evidence (Line):** `result = df.eval("x.shift(1, fill_value=-1)")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 476. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:663
- **Description:** eval()
- **Evidence (Line):** `pd.eval(ex, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 477. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:668
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval("x", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 478. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:673
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval("x", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 479. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:678
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval("x", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 480. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:684
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval("x", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 481. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:689
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval("x", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 482. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:694
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval("x", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 483. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:702
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval(exp, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 484. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:708
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval(exp, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 485. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:745
- **Description:** eval()
- **Evidence (Line):** `assert pd.eval("not True") == -2`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 486. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:746
- **Description:** eval()
- **Evidence (Line):** `assert pd.eval("not False") == -1`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 487. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:747
- **Description:** eval()
- **Evidence (Line):** `assert pd.eval("True and not True") == 0`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 488. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:752
- **Description:** eval()
- **Evidence (Line):** `assert pd.eval(f"{event.str.match('hello').a}")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 489. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:753
- **Description:** eval()
- **Evidence (Line):** `assert pd.eval(f"{event.str.match('hello').a and event.str.match('hello').a}")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 490. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:757
- **Description:** eval()
- **Evidence (Line):** `res = df.eval("a + a", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 491. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:763
- **Description:** eval()
- **Evidence (Line):** `res = pd.eval("variable_name + 0", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 492. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:784
- **Description:** eval()
- **Evidence (Line):** `res = pd.eval(s, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 493. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:794
- **Description:** eval()
- **Evidence (Line):** `tm.assert_frame_equal(res, eval(s), check_exact=False)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 494. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:816
- **Description:** eval()
- **Evidence (Line):** `res = pd.eval(s, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 495. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:839
- **Description:** eval()
- **Evidence (Line):** `res = pd.eval("df + df2", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 496. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:841
- **Description:** eval()
- **Evidence (Line):** `res = pd.eval("df + df2", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 497. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:854
- **Description:** eval()
- **Evidence (Line):** `res = pd.eval("df < 2", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 498. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:862
- **Description:** eval()
- **Evidence (Line):** `res = pd.eval("df < df3", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 499. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:890
- **Description:** eval()
- **Evidence (Line):** `res = pd.eval("df + df2 + df3", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 500. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:892
- **Description:** eval()
- **Evidence (Line):** `res = pd.eval("df + df2 + df3", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 501. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:912
- **Description:** eval()
- **Evidence (Line):** `res = pd.eval("df + s", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 502. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:914
- **Description:** eval()
- **Evidence (Line):** `res = pd.eval("df + s", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 503. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:953
- **Description:** eval()
- **Evidence (Line):** `res = pd.eval("s + df", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 504. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:955
- **Description:** eval()
- **Evidence (Line):** `res = pd.eval("s + df", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 505. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:983
- **Description:** eval()
- **Evidence (Line):** `a = pd.eval(lhs, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 506. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:985
- **Description:** eval()
- **Evidence (Line):** `b = pd.eval(rhs, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 507. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:987
- **Description:** eval()
- **Evidence (Line):** `a = pd.eval(lhs, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 508. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:988
- **Description:** eval()
- **Evidence (Line):** `b = pd.eval(rhs, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 509. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1036
- **Description:** eval()
- **Evidence (Line):** `res = pd.eval("df2 + ser + df", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 510. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1038
- **Description:** eval()
- **Evidence (Line):** `res = pd.eval("df2 + ser + df", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 511. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1054
- **Description:** eval()
- **Evidence (Line):** `pd.eval("df + s", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 512. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1058
- **Description:** eval()
- **Evidence (Line):** `pd.eval("df + s", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 513. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1063
- **Description:** eval()
- **Evidence (Line):** `pd.eval("df + s", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 514. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1076
- **Description:** eval()
- **Evidence (Line):** `pd.eval("df + s", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 515. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1095
- **Description:** eval()
- **Evidence (Line):** `def eval(self, *args, **kwargs):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 516. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1097
- **Description:** eval()
- **Evidence (Line):** `return pd.eval(*args, **kwargs)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 517. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1120
- **Description:** eval()
- **Evidence (Line):** `pd.eval(ex, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 518. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1123
- **Description:** eval()
- **Evidence (Line):** `x = self.eval(ex, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 519. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1127
- **Description:** eval()
- **Evidence (Line):** `y = self.eval(ex2, local_dict={"x": x}, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 520. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1131
- **Description:** eval()
- **Evidence (Line):** `y = self.eval(ex3, local_dict={"x": x}, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 521. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1143
- **Description:** eval()
- **Evidence (Line):** `self.eval(ex)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 522. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1146
- **Description:** eval()
- **Evidence (Line):** `res = self.eval(ex)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 523. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1147
- **Description:** eval()
- **Evidence (Line):** `exp = eval(ex)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 524. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1159
- **Description:** eval()
- **Evidence (Line):** `self.eval(ex)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 525. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1162
- **Description:** eval()
- **Evidence (Line):** `res = self.eval(ex)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 526. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1163
- **Description:** eval()
- **Evidence (Line):** `exp = eval(ex)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 527. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1171
- **Description:** eval()
- **Evidence (Line):** `self.eval("x + y", local_dict={"x": x, "y": y})`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 528. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1174
- **Description:** eval()
- **Evidence (Line):** `x = self.eval("1")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 529. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1179
- **Description:** eval()
- **Evidence (Line):** `df2 = self.eval("df", local_dict={"df": df})`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 530. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1185
- **Description:** eval()
- **Evidence (Line):** `self.eval("df[x > 2] > 2")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 531. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1189
- **Description:** eval()
- **Evidence (Line):** `result = self.eval("(df + 1)[df > 2]", local_dict={"df": df})`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 532. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1206
- **Description:** eval()
- **Evidence (Line):** `tm.assert_series_equal(expec, self.eval(e, local_dict={"df": df}))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 533. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1216
- **Description:** eval()
- **Evidence (Line):** `self.eval(expr1, local_dict={"df": df, "df2": df2})`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 534. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1224
- **Description:** eval()
- **Evidence (Line):** `df.eval("d c = a + b")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 535. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1233
- **Description:** eval()
- **Evidence (Line):** `df.eval("d,c = a + b")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 536. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1241
- **Description:** eval()
- **Evidence (Line):** `df.eval('Timestamp("20131001") = a + b')`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 537. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1250
- **Description:** eval()
- **Evidence (Line):** `df.eval("a = a + b", inplace=True)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 538. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1260
- **Description:** eval()
- **Evidence (Line):** `df.eval("c = a + b", inplace=True)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 539. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1269
- **Description:** eval()
- **Evidence (Line):** `df.eval("a = 1 + b", inplace=True)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 540. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1282
- **Description:** eval()
- **Evidence (Line):** `df.eval("a = a + b", inplace=True)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 541. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1292
- **Description:** eval()
- **Evidence (Line):** `df.eval("c = a + b", inplace=True)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 542. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1295
- **Description:** eval()
- **Evidence (Line):** `df.eval("c = a = b")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 543. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1302
- **Description:** eval()
- **Evidence (Line):** `self.eval("c = df.a + df.b", local_dict={"df": df}, target=df, inplace=True)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 544. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1310
- **Description:** eval()
- **Evidence (Line):** `result = df.eval("a in [11, -32]", engine=engine)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 545. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1321
- **Description:** eval()
- **Evidence (Line):** `actual = df.eval("c = a + b", inplace=False)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 546. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1335
- **Description:** eval()
- **Evidence (Line):** `answer = df.eval(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 547. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1346
- **Description:** eval()
- **Evidence (Line):** `answer = df.eval(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 548. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1358
- **Description:** eval()
- **Evidence (Line):** `df.eval(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 549. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1372
- **Description:** eval()
- **Evidence (Line):** `df = df.eval(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 550. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1382
- **Description:** eval()
- **Evidence (Line):** `df = df.eval(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 551. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1398
- **Description:** eval()
- **Evidence (Line):** `answer = df.eval(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 552. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1418
- **Description:** eval()
- **Evidence (Line):** `answer = df.eval(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 553. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1438
- **Description:** eval()
- **Evidence (Line):** `answer = df.eval(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 554. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1468
- **Description:** eval()
- **Evidence (Line):** `self.eval("a = 1 + 2", target=df, inplace=True)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 555. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1477
- **Description:** eval()
- **Evidence (Line):** `self.eval(expression, target=invalid_target, inplace=True)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 556. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1481
- **Description:** eval()
- **Evidence (Line):** `self.eval(expression, target=invalid_target, inplace=False)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 557. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1489
- **Description:** eval()
- **Evidence (Line):** `self.eval(expression, target=invalid_target, inplace=False)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 558. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1495
- **Description:** eval()
- **Evidence (Line):** `assert self.eval(expression, target=target, inplace=False) == 3`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 559. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1499
- **Description:** eval()
- **Evidence (Line):** `self.eval(expression, target=target, inplace=True)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 560. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1507
- **Description:** eval()
- **Evidence (Line):** `r = self.eval("df < 2", local_dict={"df": df})`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 561. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1518
- **Description:** eval()
- **Evidence (Line):** `r = self.eval("df[df < 2 + 3]", local_dict={"df": df})`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 562. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1527
- **Description:** eval()
- **Evidence (Line):** `r = self.eval("df[df[df < 2] < 2] + df * 2", local_dict={"df": df})`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 563. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1534
- **Description:** eval()
- **Evidence (Line):** `res = self.eval(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 564. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1545
- **Description:** eval()
- **Evidence (Line):** `res = pd.eval("1 in [1, 2]", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 565. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1548
- **Description:** eval()
- **Evidence (Line):** `res = pd.eval("2 in (1, 2)", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 566. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1551
- **Description:** eval()
- **Evidence (Line):** `res = pd.eval("3 in (1, 2)", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 567. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1554
- **Description:** eval()
- **Evidence (Line):** `res = pd.eval("3 not in (1, 2)", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 568. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1557
- **Description:** eval()
- **Evidence (Line):** `res = pd.eval("[3] not in (1, 2)", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 569. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1560
- **Description:** eval()
- **Evidence (Line):** `res = pd.eval("[3] in ([3], 2)", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 570. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1563
- **Description:** eval()
- **Evidence (Line):** `res = pd.eval("[[3]] in [[[3]], 2]", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 571. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1566
- **Description:** eval()
- **Evidence (Line):** `res = pd.eval("(3,) in [(3,), 2]", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 572. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1569
- **Description:** eval()
- **Evidence (Line):** `res = pd.eval("(3,) not in [(3,), 2]", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 573. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1572
- **Description:** eval()
- **Evidence (Line):** `res = pd.eval("[(3,)] in [[(3,)], 2]", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 574. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1577
- **Description:** eval()
- **Evidence (Line):** `pd.eval("1 in [1, 2]", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 575. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1579
- **Description:** eval()
- **Evidence (Line):** `pd.eval("2 in (1, 2)", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 576. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1581
- **Description:** eval()
- **Evidence (Line):** `pd.eval("3 in (1, 2)", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 577. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1583
- **Description:** eval()
- **Evidence (Line):** `pd.eval("[(3,)] in (1, 2, [(3,)])", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 578. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1586
- **Description:** eval()
- **Evidence (Line):** `pd.eval("3 not in (1, 2)", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 579. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1588
- **Description:** eval()
- **Evidence (Line):** `pd.eval("[3] not in (1, 2, [[3]])", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 580. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1594
- **Description:** eval()
- **Evidence (Line):** `res = pd.eval(expr, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 581. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1613
- **Description:** eval()
- **Evidence (Line):** `pd.eval(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 582. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1621
- **Description:** eval()
- **Evidence (Line):** `pd.eval(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 583. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1635
- **Description:** eval()
- **Evidence (Line):** `pd.eval(ex, parser=parser, engine=engine)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 584. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1638
- **Description:** eval()
- **Evidence (Line):** `pd.eval(ex, parser=parser, engine=engine)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 585. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1642
- **Description:** eval()
- **Evidence (Line):** `def eval(self, *args, **kwargs):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 586. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1644
- **Description:** eval()
- **Evidence (Line):** `return pd.eval(*args, **kwargs)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 587. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1653
- **Description:** eval()
- **Evidence (Line):** `got = self.eval(expr, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 588. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1670
- **Description:** eval()
- **Evidence (Line):** `got = self.eval(expr, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 589. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1682
- **Description:** eval()
- **Evidence (Line):** `df.eval(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 590. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1699
- **Description:** eval()
- **Evidence (Line):** `df.eval("e = sin(a + b)", engine=engine, parser=parser, inplace=True)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 591. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1724
- **Description:** eval()
- **Evidence (Line):** `df.eval("b = sin(a)", engine=engine, parser=parser, inplace=True)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 592. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1736
- **Description:** eval()
- **Evidence (Line):** `df.eval("mysin(a)", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 593. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1743
- **Description:** eval()
- **Evidence (Line):** `df.eval("sin(x=a)", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 594. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1753
- **Description:** eval()
- **Evidence (Line):** `_var_s * 2, pd.eval(e, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 595. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1759
- **Description:** eval()
- **Evidence (Line):** `pd.eval("x + 1", local_dict=lcls, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 596. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1767
- **Description:** eval()
- **Evidence (Line):** `pd.eval("x + 1", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 597. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1776
- **Description:** eval()
- **Evidence (Line):** `pd.eval("x + 1", engine=engine, parser=parser, local_dict={})`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 598. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1783
- **Description:** eval()
- **Evidence (Line):** `pd.eval(e, engine=engine, parser=parser, global_dict={})`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 599. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1790
- **Description:** eval()
- **Evidence (Line):** `pd.eval("x + y", local_dict={"x": 1, "y": 2}, engine="asdf")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 600. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1826
- **Description:** eval()
- **Evidence (Line):** `pd.eval("x + y", local_dict={"x": 1, "y": 2}, parser="asdf")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 601. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1851
- **Description:** eval()
- **Evidence (Line):** `pd.eval(e, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 602. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1858
- **Description:** eval()
- **Evidence (Line):** `pd.eval(e, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 603. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1867
- **Description:** eval()
- **Evidence (Line):** `pd.eval(express, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 604. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1870
- **Description:** eval()
- **Evidence (Line):** `pd.eval(express, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 605. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1878
- **Description:** eval()
- **Evidence (Line):** `pd.eval("sin + dotted_line", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 606. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1880
- **Description:** eval()
- **Evidence (Line):** `res = pd.eval("sin + dotted_line", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 607. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1887
- **Description:** eval()
- **Evidence (Line):** `pd.eval("1 + 2", resolvers=cannot_resolve, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 608. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1893
- **Description:** eval()
- **Evidence (Line):** `pd.eval("", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 609. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1898
- **Description:** eval()
- **Evidence (Line):** `pd.eval("1 + 1; 2 + 2", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 610. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1920
- **Description:** eval()
- **Evidence (Line):** `pd.eval(ex, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 611. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1932
- **Description:** eval()
- **Evidence (Line):** `result = df.eval(f"A == {other}")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 612. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:1940
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval(s, engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 613. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:2003
- **Description:** eval()
- **Evidence (Line):** `df.eval("A = B + C", inplace=True)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 614. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:2015
- **Description:** eval()
- **Evidence (Line):** `pd.eval("2+2", inplace=value)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 615. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:2021
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval("1 / 2", engine="numexpr")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 616. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:2032
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval("(x + y).dropna()")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 617. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:2037
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval("(x * y).dropna()")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 618. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:2042
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval("(x + y).dropna().reset_index(drop=True)")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 619. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:2050
- **Description:** eval()
- **Evidence (Line):** `df.eval("new = old", inplace=True, engine=engine)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 620. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/computation/test_eval.py:2063
- **Description:** eval()
- **Evidence (Line):** `result = df.eval("new = old", engine=engine)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 621. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/copy_view/test_astype.py:113
- **Description:** pickle load/dumps
- **Evidence (Line):** `base_copy = pickle.loads(pickle.dumps(base))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 622. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/copy_view/test_astype.py:122
- **Description:** pickle load/dumps
- **Evidence (Line):** `base_copy = pickle.loads(pickle.dumps(base))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 623. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/copy_view/test_astype.py:131
- **Description:** pickle load/dumps
- **Evidence (Line):** `base_copy = pickle.loads(pickle.dumps(base))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 624. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/copy_view/test_methods.py:1530
- **Description:** eval()
- **Evidence (Line):** `def test_eval():`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 625. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/copy_view/test_methods.py:1534
- **Description:** eval()
- **Evidence (Line):** `result = df.eval("c = a+b")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 626. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/copy_view/test_methods.py:1546
- **Description:** eval()
- **Evidence (Line):** `df.eval("c = a+b", inplace=True)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 627. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/extension/test_arrow.py:1559
- **Description:** pickle load/dumps
- **Evidence (Line):** `result = pickle.loads(full_pickled)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 628. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/extension/test_arrow.py:1562
- **Description:** pickle load/dumps
- **Evidence (Line):** `result_sliced = pickle.loads(sliced_pickled)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 629. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/extension/test_arrow.py:3325
- **Description:** pickle load/dumps
- **Evidence (Line):** `result = pickle.loads(pickle.dumps(expected))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 630. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/methods/test_sample.py:198
- **Description:** eval()
- **Evidence (Line):** `result = obj.sample(n=3, random_state=eval(func_str)(arg))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 631. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/methods/test_sample.py:199
- **Description:** eval()
- **Evidence (Line):** `expected = obj.sample(n=3, random_state=com.random_state(eval(func_str)(arg)))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 632. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:61
- **Description:** eval()
- **Evidence (Line):** `result = df.eval("A+1")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 633. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:67
- **Description:** eval()
- **Evidence (Line):** `result = df.eval("A+1", engine=None)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 634. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:73
- **Description:** eval()
- **Evidence (Line):** `result = df.eval("A+1", engine="python")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 635. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:80
- **Description:** eval()
- **Evidence (Line):** `result = df.eval("A+1", engine="numexpr")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 636. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:91
- **Description:** eval()
- **Evidence (Line):** `df.eval("A+1", engine="numexpr")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 637. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:118
- **Description:** eval()
- **Evidence (Line):** `expected = eval(f"base {op_str} df")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 638. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:121
- **Description:** eval()
- **Evidence (Line):** `result = eval(f"m {op_str} df")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 639. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:180
- **Description:** eval()
- **Evidence (Line):** `assert df.eval("a + b", resolvers=[dict1, dict2]) == dict1["a"] + dict2["b"]`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 640. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:181
- **Description:** eval()
- **Evidence (Line):** `assert pd.eval("a + b", resolvers=[dict1, dict2]) == dict1["a"] + dict2["b"]`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 641. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:191
- **Description:** eval()
- **Evidence (Line):** `result = df.eval("a + b * c", resolvers=[dict1])`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 642. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:199
- **Description:** eval()
- **Evidence (Line):** `res = df.eval("c = ((a1 == 'Y') & True)")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 643. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:207
- **Description:** eval()
- **Evidence (Line):** `res = df.eval("@np.floor(a)", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 644. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:213
- **Description:** eval()
- **Evidence (Line):** `res = df.eval("a", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 645. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:217
- **Description:** eval()
- **Evidence (Line):** `def test_extension_array_eval(self, engine, parser, request):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 646. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:225
- **Description:** eval()
- **Evidence (Line):** `result = df.eval("a / b", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 647. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:229
- **Description:** eval()
- **Evidence (Line):** `def test_complex_eval(self, engine, parser):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 648. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:232
- **Description:** eval()
- **Evidence (Line):** `result = df.eval("a/b", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 649. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:649
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval("df[df > 0 and df2 > 0]", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 650. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:652
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 651. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:658
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval("df[(df>0) & (df2>0)]", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 652. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:900
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval("x + 1", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 653. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:915
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval("df[(df > 0) & (df2 > 0)]", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 654. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:919
- **Description:** eval()
- **Evidence (Line):** `result = pd.eval(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 655. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:1206
- **Description:** eval()
- **Evidence (Line):** `res = frame.eval("a + b", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 656. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:1211
- **Description:** eval()
- **Evidence (Line):** `res = frame.eval("a[a < 1] + b", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 657. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:1221
- **Description:** eval()
- **Evidence (Line):** `df.eval(f"a {op} b", engine=engine, parser=parser)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 658. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:1272
- **Description:** eval()
- **Evidence (Line):** `res = df.eval("A + `B B`")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 659. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:1277
- **Description:** eval()
- **Evidence (Line):** `res = df.eval("`B B` + `C C`")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 660. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:1282
- **Description:** eval()
- **Evidence (Line):** `res = df.eval("`C_C` + A")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 661. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:1287
- **Description:** eval()
- **Evidence (Line):** `res = df.eval("C_C + `C C`")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 662. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:1292
- **Description:** eval()
- **Evidence (Line):** `res = df.eval("A + `D_D D`")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 663. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:1297
- **Description:** eval()
- **Evidence (Line):** `res = df.eval("A + `C_C`")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 664. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:1302
- **Description:** eval()
- **Evidence (Line):** `res = df.eval("`E.E` + `F-F` - A")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 665. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:1307
- **Description:** eval()
- **Evidence (Line):** `res = df.eval("A + `1e1`")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 666. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:1312
- **Description:** eval()
- **Evidence (Line):** `res = df.eval("A + `def`")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 667. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:1337
- **Description:** eval()
- **Evidence (Line):** `res = df.eval("` A` + `  `")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 668. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:1354
- **Description:** eval()
- **Evidence (Line):** `df.eval("@pd.thing")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 669. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:1519
- **Description:** eval()
- **Evidence (Line):** `df.eval("@func()")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 670. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:1522
- **Description:** eval()
- **Evidence (Line):** `df.eval("@funcs[0]()")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 671. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:1525
- **Description:** eval()
- **Evidence (Line):** `df.eval("@funcs[0].__call__()")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 672. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:1534
- **Description:** eval()
- **Evidence (Line):** `result = df.eval("c = b - a")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 673. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:1547
- **Description:** eval()
- **Evidence (Line):** `result = df.eval("c = b - 1")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 674. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/frame/test_query_eval.py:1558
- **Description:** eval()
- **Evidence (Line):** `result = df.eval("c = 2 - 1")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 675. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/generic/test_finalize.py:390
- **Description:** eval()
- **Evidence (Line):** `result = df.eval("A + 1", engine="numexpr")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 676. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/indexes/base_class/test_formats.py:15
- **Description:** eval()
- **Evidence (Line):** `res = eval(repr(idx))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 677. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/indexes/categorical/test_category.py:207
- **Description:** eval()
- **Evidence (Line):** `tm.assert_index_equal(eval(repr(ci)), ci, exact=True)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 678. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/indexes/multi/test_formats.py:22
- **Description:** eval()
- **Evidence (Line):** `eval(repr(mi))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 679. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/indexes/numeric/test_numeric.py:37
- **Description:** eval()
- **Evidence (Line):** `tm.assert_index_equal(eval(repr(index)), index, exact=True)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 680. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/indexes/ranges/test_range.py:64
- **Description:** eval()
- **Evidence (Line):** `result = eval(result)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 681. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/indexes/ranges/test_range.py:72
- **Description:** eval()
- **Evidence (Line):** `result = eval(result)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 682. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/indexes/ranges/test_range.py:392
- **Description:** eval()
- **Evidence (Line):** `tm.assert_index_equal(eval(repr(index)), index)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 683. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/indexes/test_old_base.py:236
- **Description:** eval()
- **Evidence (Line):** `tm.assert_index_equal(eval(repr(idx)), idx)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 684. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/io/test_pickle.py:212
- **Description:** pickle load/dumps
- **Evidence (Line):** `return pickle.load(fh)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 685. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/io/test_pickle.py:587
- **Description:** pickle load/dumps
- **Evidence (Line):** `df = pickle.load(fd)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 686. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/io/xml/test_to_xml.py:1090
- **Description:** eval()
- **Evidence (Line):** `def test_incorrect_xsl_eval(geom_df):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 687. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/io/xml/test_xml.py:1277
- **Description:** eval()
- **Evidence (Line):** `def test_incorrect_xsl_eval(kml_cta_rail_lines):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 688. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/libs/test_lib.py:295
- **Description:** pickle load/dumps
- **Evidence (Line):** `arr = pickle.loads(pickle.dumps(arr))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 689. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/scalar/test_na_scalar.py:316
- **Description:** pickle load/dumps
- **Evidence (Line):** `result = pickle.loads(pickle.dumps(NA))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 690. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/scalar/timestamp/test_constructors.py:690
- **Description:** eval()
- **Evidence (Line):** `assert result == eval(repr(result))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 691. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/scalar/timestamp/test_constructors.py:698
- **Description:** eval()
- **Evidence (Line):** `assert result == eval(repr(result))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 692. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/scalar/timestamp/test_constructors.py:707
- **Description:** eval()
- **Evidence (Line):** `assert result == eval(repr(result))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 693. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/scalar/timestamp/test_constructors.py:715
- **Description:** eval()
- **Evidence (Line):** `assert result == eval(repr(result))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 694. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/scalar/timestamp/test_formats.py:115
- **Description:** eval()
- **Evidence (Line):** `assert date_only == eval(repr(date_only))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 695. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/scalar/timestamp/test_formats.py:121
- **Description:** eval()
- **Evidence (Line):** `assert date_tz == eval(repr(date_tz))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 696. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/scalar/timestamp/test_formats.py:131
- **Description:** eval()
- **Evidence (Line):** `assert date_with_utc_offset == eval(expr)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 697. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/scalar/timestamp/test_formats.py:168
- **Description:** eval()
- **Evidence (Line):** `assert eval(repr(z)) == z`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 698. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/test_downstream.py:129
- **Description:** pickle load/dumps
- **Evidence (Line):** `"pickle.loads(pickle.dumps(pd.date_range('2021-01-01', periods=1)))"`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 699. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/test_downstream.py:181
- **Description:** yaml.load (unsafe)
- **Evidence (Line):** `loaded = yaml.load(dumped, Loader=yaml.Loader)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 700. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/test_downstream.py:184
- **Description:** yaml.load (unsafe)
- **Evidence (Line):** `loaded2 = yaml.load(dumped, Loader=yaml.UnsafeLoader)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 701. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pluggy/_caller.py:197
- **Description:** exec()
- **Evidence (Line):** `return self._hookexec(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 702. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pluggy/_caller.py:222
- **Description:** exec()
- **Evidence (Line):** `res = self._hookexec(self.name, self._hookimpls.copy(), kwargs, False)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 703. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pluggy/_caller.py:262
- **Description:** exec()
- **Evidence (Line):** `return self._hookexec(self.name, hookimpls, kwargs, firstresult)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 704. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pluggy/_caller.py:269
- **Description:** exec()
- **Evidence (Line):** `res = self._hookexec(self.name, [method], kwargs, False)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 705. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pluggy/_manager.py:174
- **Description:** exec()
- **Evidence (Line):** `def _hookexec(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 706. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pluggy/_manager.py:183
- **Description:** exec()
- **Evidence (Line):** `return self._inner_hookexec(hook_name, methods, kwargs, firstresult)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 707. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pluggy/_manager.py:587
- **Description:** exec()
- **Evidence (Line):** `def traced_hookexec(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 708. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pyarrow/tests/test_flight.py:2389
- **Description:** eval()
- **Evidence (Line):** `client_headers = ast.literal_eval(raw_headers)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 709. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pydantic/_internal/_decorators.py:599
- **Description:** eval()
- **Evidence (Line):** `sig = signature_no_eval(validator)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 710. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pydantic/_internal/_decorators.py:637
- **Description:** eval()
- **Evidence (Line):** `sig = signature_no_eval(serializer)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 711. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pydantic/_internal/_decorators.py:675
- **Description:** eval()
- **Evidence (Line):** `sig = signature_no_eval(serializer)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 712. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pydantic/_internal/_decorators.py:707
- **Description:** eval()
- **Evidence (Line):** `sig = signature_no_eval(serializer)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 713. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pydantic/_internal/_decorators.py:755
- **Description:** eval()
- **Evidence (Line):** `sig = signature_no_eval(unwrap_wrapped_function(function))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 714. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pydantic/_internal/_decorators.py:779
- **Description:** eval()
- **Evidence (Line):** `sig = signature_no_eval(unwrap_wrapped_function(function))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 715. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pydantic/_internal/_fields.py:849
- **Description:** eval()
- **Evidence (Line):** `sig = _typing_extra.signature_no_eval(default_factory)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 716. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pydantic/_internal/_generate_schema.py:2030
- **Description:** eval()
- **Evidence (Line):** `sig = _typing_extra.signature_no_eval(function)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 717. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pydantic/_internal/_generate_schema.py:2055
- **Description:** eval()
- **Evidence (Line):** `sig = _typing_extra.signature_no_eval(function)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 718. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pydantic/_internal/_generate_schema.py:2134
- **Description:** eval()
- **Evidence (Line):** `sig = _typing_extra.signature_no_eval(function)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 719. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pydantic/_internal/_namespace_utils.py:38
- **Description:** eval()
- **Evidence (Line):** `return eval(typ, *ns)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 720. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pydantic/_internal/_signature.py:96
- **Description:** eval()
- **Evidence (Line):** `present_params = signature_no_eval(init).parameters.values()`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 721. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pydantic/_internal/_typing_extra.py:458
- **Description:** eval()
- **Evidence (Line):** `def signature_no_eval(f: Callable[..., Any]) -> Signature:`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 722. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pydantic/_internal/_validate_call.py:107
- **Description:** eval()
- **Evidence (Line):** `signature = signature_no_eval(self.function)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 723. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/pydantic/deprecated/parse.py:55
- **Description:** pickle load/dumps
- **Evidence (Line):** `return pickle.loads(bb)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 724. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pydantic/json_schema.py:1836
- **Description:** eval()
- **Evidence (Line):** `if len(_typing_extra.signature_no_eval(json_schema_extra).parameters) > 1:`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 725. [Critical] Hardcoded Secret
- **File:** .venv-test/lib/python3.12/site-packages/pydantic/types.py:1835
- **Description:** Password Assignment detected
- **Evidence (Line):** `user = User(username='scolvin', password='password1')`
- **Exploit Scenario:** Attacker could extract credentials and gain unauthorized access
- **Fix Recommendation:** Move secrets to environment variables or secret manager, rotate compromised credentials
- **Confidence:** High

### 726. [Critical] Hardcoded Secret
- **File:** .venv-test/lib/python3.12/site-packages/pydantic/types.py:1862
- **Description:** Password Assignment detected
- **Evidence (Line):** `model = Model(password='IAmSensitive', password_bytes=b'IAmSensitiveBytes')`
- **Exploit Scenario:** Attacker could extract credentials and gain unauthorized access
- **Fix Recommendation:** Move secrets to environment variables or secret manager, rotate compromised credentials
- **Confidence:** High

### 727. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/pydantic/v1/parse.py:42
- **Description:** pickle load/dumps
- **Evidence (Line):** `return pickle.loads(bb)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 728. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pydantic/v1/utils.py:195
- **Description:** eval()
- **Evidence (Line):** `eval('__IPYTHON__')`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 729. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pydantic/validate_call_decorator.py:29
- **Description:** eval()
- **Evidence (Line):** `_typing_extra.signature_no_eval(cast(_generate_schema.ValidateCallSupportedTypes, function))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 730. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pygments/formatters/__init__.py:91
- **Description:** eval()
- **Evidence (Line):** `this method is equivalent to running ``eval()`` on the input file. The formatter is`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 731. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pygments/formatters/__init__.py:103
- **Description:** exec()
- **Evidence (Line):** `exec(f.read(), custom_namespace)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 732. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pygments/lexers/__init__.py:154
- **Description:** exec()
- **Evidence (Line):** `exec(f.read(), custom_namespace)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 733. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pygments/lexers/_julia_builtins.py:150
- **Description:** eval()
- **Evidence (Line):** `v = eval(Symbol(compl.mod))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 734. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pygments/lexers/_julia_builtins.py:361
- **Description:** eval()
- **Evidence (Line):** `v = eval(Symbol(compl.mod))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 735. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/pygments/lexers/special.py:115
- **Description:** eval()
- **Evidence (Line):** `val = ast.literal_eval(val)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 736. [Critical] Hardcoded Secret
- **File:** .venv-test/lib/python3.12/site-packages/ragas/cli.py:792
- **Description:** API Key Assignment detected
- **Evidence (Line):** `export ANTHROPIC_API_KEY="your-anthropic-key"`
- **Exploit Scenario:** Attacker could extract credentials and gain unauthorized access
- **Fix Recommendation:** Move secrets to environment variables or secret manager, rotate compromised credentials
- **Confidence:** High

### 737. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/ragas/integrations/langchain.py:143
- **Description:** eval()
- **Evidence (Line):** `def _validate_langsmith_eval(self, run: Run, example: t.Optional[Example]) -> None:`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 738. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/ragas/integrations/langchain.py:184
- **Description:** eval()
- **Evidence (Line):** `self._validate_langsmith_eval(run, example)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 739. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/regex/tests/test_regex.py:3775
- **Description:** pickle load/dumps
- **Evidence (Line):** `r = pickle.loads(p)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 740. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/rich/markup.py:190
- **Description:** eval()
- **Evidence (Line):** `meta_params = literal_eval(parameters)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 741. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/_external/array_api_compat/_internal.py:64
- **Description:** exec()
- **Evidence (Line):** `exec(f"from {mod.__name__} import *", objs)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 742. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/_external/array_api_compat/cupy/fft.py:7
- **Description:** exec()
- **Evidence (Line):** `exec("from cupy.fft import *", _n)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 743. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/_external/array_api_compat/cupy/linalg.py:10
- **Description:** exec()
- **Evidence (Line):** `exec('from cupy.linalg import *', _n)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 744. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/_external/cobyqa/main.py:650
- **Description:** eval()
- **Evidence (Line):** `fun_val, cub_val, ceq_val = _eval(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 745. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/_external/cobyqa/main.py:697
- **Description:** eval()
- **Evidence (Line):** `fun_val, cub_val, ceq_val = _eval(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 746. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/_external/cobyqa/main.py:840
- **Description:** eval()
- **Evidence (Line):** `fun_val, cub_val, ceq_val = _eval(pb, framework, step, options)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 747. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/_external/cobyqa/main.py:1422
- **Description:** eval()
- **Evidence (Line):** `def _eval(pb, framework, step, options):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 748. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/_external/cobyqa/main.py:1446
- **Description:** eval()
- **Evidence (Line):** `x, fun, maxcv = pb.best_eval(penalty)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 749. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/_external/cobyqa/problem.py:80
- **Description:** eval()
- **Evidence (Line):** `def n_eval(self):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 750. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/_external/cobyqa/problem.py:560
- **Description:** eval()
- **Evidence (Line):** `def n_eval(self):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 751. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/_external/cobyqa/problem.py:886
- **Description:** eval()
- **Evidence (Line):** `x_best, fun_best, _ = self.best_eval(penalty)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 752. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/_external/cobyqa/problem.py:947
- **Description:** eval()
- **Evidence (Line):** `def n_eval(self):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 753. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/_external/cobyqa/problem.py:1192
- **Description:** eval()
- **Evidence (Line):** `def best_eval(self, penalty):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 754. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/_lib/_bunch.py:160
- **Description:** exec()
- **Evidence (Line):** `exec(s, namespace)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 755. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/_lib/_elementwise_iterative_method.py:238
- **Description:** eval()
- **Evidence (Line):** `x = pre_func_eval(work)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 756. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/_lib/_elementwise_iterative_method.py:261
- **Description:** eval()
- **Evidence (Line):** `post_func_eval(x, f, work)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 757. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/scipy/_lib/tests/test_bunch.py:59
- **Description:** pickle load/dumps
- **Evidence (Line):** `obj = pickle.loads(s)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 758. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/scipy/datasets/_fetchers.py:79
- **Description:** pickle load/dumps
- **Evidence (Line):** `ascent = array(pickle.load(f))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 759. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/differentiate/_differentiate.py:449
- **Description:** eval()
- **Evidence (Line):** `def pre_func_eval(work):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 760. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/differentiate/_differentiate.py:495
- **Description:** eval()
- **Evidence (Line):** `def post_func_eval(x, f, work):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 761. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/integrate/_ivp/tests/test_ivp.py:700
- **Description:** eval()
- **Evidence (Line):** `def test_t_eval():`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 762. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/integrate/_tanhsinh.py:399
- **Description:** eval()
- **Evidence (Line):** `def pre_func_eval(work):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 763. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/integrate/_tanhsinh.py:413
- **Description:** eval()
- **Evidence (Line):** `def post_func_eval(x, fj, work):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 764. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/integrate/tests/test__quad_vec.py:146
- **Description:** eval()
- **Evidence (Line):** `def test_num_eval(self, quadrature):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 765. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/interpolate/tests/test_bsplines.py:160
- **Description:** eval()
- **Evidence (Line):** `def test_rndm_naive_eval(self, xp):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 766. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/interpolate/tests/test_bsplines.py:167
- **Description:** eval()
- **Evidence (Line):** `y_n = xp.stack([_naive_eval(x, t, c, k, xp=xp) for x in xx])`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 767. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/interpolate/tests/test_bsplines.py:941
- **Description:** eval()
- **Evidence (Line):** `def _naive_eval(x, t, c, k, *, xp):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 768. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/interpolate/tests/test_bsplines.py:1417
- **Description:** eval()
- **Evidence (Line):** `b1 = np.vectorize(lambda x: _naive_eval(x, t, c, k, xp=np))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 769. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/interpolate/tests/test_fitpack2.py:1586
- **Description:** eval()
- **Evidence (Line):** `z_spl = spl_eval(spl, x, y)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 770. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/interpolate/tests/test_fitpack2.py:1615
- **Description:** eval()
- **Evidence (Line):** `z_spl = spl_eval(spl, x, y)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 771. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/interpolate/tests/test_fitpack2.py:1651
- **Description:** eval()
- **Evidence (Line):** `z_spl = spl_eval(spl, x, y)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 772. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/scipy/interpolate/tests/test_interpnd.py:172
- **Description:** pickle load/dumps
- **Evidence (Line):** `ip2 = pickle.loads(pickle.dumps(ip))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 773. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/scipy/interpolate/tests/test_interpnd.py:413
- **Description:** pickle load/dumps
- **Evidence (Line):** `ip2 = pickle.loads(pickle.dumps(ip))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 774. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/interpolate/tests/test_interpolate.py:858
- **Description:** eval()
- **Evidence (Line):** `def test_eval(self, xp):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 775. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/interpolate/tests/test_interpolate.py:1460
- **Description:** eval()
- **Evidence (Line):** `def test_derivative_eval(self, xp):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 776. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/interpolate/tests/test_interpolate.py:2440
- **Description:** eval()
- **Evidence (Line):** `v2 = _ppoly2d_eval(c, (x, y), xi, yi)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 777. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/interpolate/tests/test_interpolate.py:2446
- **Description:** eval()
- **Evidence (Line):** `v2 = _ppoly2d_eval(c, (x, y), xi, yi, nu=nu)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 778. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/interpolate/tests/test_interpolate.py:2466
- **Description:** eval()
- **Evidence (Line):** `v2 = _ppoly3d_eval(c, (x, y, z), xi, yi, zi, nu=nu)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 779. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/interpolate/tests/test_interpolate.py:2486
- **Description:** eval()
- **Evidence (Line):** `v2 = _ppoly4d_eval(c, (x, y, z, u), xi, yi, zi, ui)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 780. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/interpolate/tests/test_interpolate.py:2689
- **Description:** eval()
- **Evidence (Line):** `def _ppoly2d_eval(c, xs, xnew, ynew, nu=None):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 781. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/interpolate/tests/test_interpolate.py:2725
- **Description:** eval()
- **Evidence (Line):** `def _ppoly3d_eval(c, xs, xnew, ynew, znew, nu=None):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 782. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/interpolate/tests/test_interpolate.py:2765
- **Description:** eval()
- **Evidence (Line):** `def _ppoly4d_eval(c, xs, xnew, ynew, znew, unew, nu=None):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 783. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/scipy/interpolate/tests/test_interpolate.py:2825
- **Description:** pickle load/dumps
- **Evidence (Line):** `y2 = pickle.loads(pickle.dumps(obj))(x_eval)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 784. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/scipy/interpolate/tests/test_interpolate.py:2850
- **Description:** pickle load/dumps
- **Evidence (Line):** `Z2 = pickle.loads(pickle.dumps(obj))(eval_points)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 785. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/interpolate/tests/test_polyint.py:789
- **Description:** eval()
- **Evidence (Line):** `def test_periodic_eval(self, xp):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 786. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/scipy/interpolate/tests/test_rbfinterp.py:459
- **Description:** pickle load/dumps
- **Evidence (Line):** `yitp2 = pickle.loads(pickle.dumps(interp))(xitp)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 787. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/scipy/odr/tests/test_odr.py:575
- **Description:** pickle load/dumps
- **Evidence (Line):** `pickle.loads(obj_pickle)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 788. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/scipy/odr/tests/test_odr.py:584
- **Description:** pickle load/dumps
- **Evidence (Line):** `pickle.loads(obj_pickle)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 789. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/scipy/odr/tests/test_odr.py:588
- **Description:** pickle load/dumps
- **Evidence (Line):** `pickle.loads(obj_pickle)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 790. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/scipy/odr/tests/test_odr.py:597
- **Description:** pickle load/dumps
- **Evidence (Line):** `pickle.loads(obj_pickle)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 791. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/scipy/odr/tests/test_odr.py:606
- **Description:** pickle load/dumps
- **Evidence (Line):** `pickle.loads(obj_pickle)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 792. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/optimize/_bracket.py:244
- **Description:** eval()
- **Evidence (Line):** `def pre_func_eval(work):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 793. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/optimize/_bracket.py:262
- **Description:** eval()
- **Evidence (Line):** `def post_func_eval(x, f, work):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 794. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/optimize/_bracket.py:653
- **Description:** eval()
- **Evidence (Line):** `def pre_func_eval(work):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 795. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/optimize/_bracket.py:669
- **Description:** eval()
- **Evidence (Line):** `def post_func_eval(x, f, work):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 796. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/optimize/_chandrupatla.py:152
- **Description:** eval()
- **Evidence (Line):** `def pre_func_eval(work):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 797. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/optimize/_chandrupatla.py:157
- **Description:** eval()
- **Evidence (Line):** `def post_func_eval(x, f, work):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 798. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/optimize/_chandrupatla.py:427
- **Description:** eval()
- **Evidence (Line):** `def pre_func_eval(work):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 799. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/optimize/_chandrupatla.py:464
- **Description:** eval()
- **Evidence (Line):** `def post_func_eval(x, f, work):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 800. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/optimize/_nonlin.py:1642
- **Description:** exec()
- **Evidence (Line):** `exec(wrapper, ns)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 801. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/optimize/_optimize.py:323
- **Description:** eval()
- **Evidence (Line):** `def eval(x):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 802. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/optimize/tests/test__differential_evolution.py:261
- **Description:** eval()
- **Evidence (Line):** `def test_best_solution_retrieval(self):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 803. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/optimize/tests/test_constraints.py:183
- **Description:** eval()
- **Evidence (Line):** `bounds2 = eval(repr(Bounds(*args)))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 804. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/signal/_spline_filters.py:342
- **Description:** eval()
- **Evidence (Line):** `>>> filtered = cspline1d_eval(cspline1d(sig), time)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 805. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/signal/_spline_filters.py:396
- **Description:** eval()
- **Evidence (Line):** `>>> filtered = qspline1d_eval(qspline1d(sig), time)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 806. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/signal/_spline_filters.py:526
- **Description:** eval()
- **Evidence (Line):** `def cspline1d_eval(cj, newx, dx=1.0, x0=0):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 807. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/signal/_spline_filters.py:569
- **Description:** eval()
- **Evidence (Line):** `>>> filtered = cspline1d_eval(cspline1d(sig), time)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 808. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/signal/_spline_filters.py:592
- **Description:** eval()
- **Evidence (Line):** `res[cond1] = cspline1d_eval(cj, -newx[cond1])`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 809. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/signal/_spline_filters.py:593
- **Description:** eval()
- **Evidence (Line):** `res[cond2] = cspline1d_eval(cj, 2 * (N - 1) - newx[cond2])`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 810. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/signal/_spline_filters.py:607
- **Description:** eval()
- **Evidence (Line):** `def qspline1d_eval(cj, newx, dx=1.0, x0=0):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 811. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/signal/_spline_filters.py:652
- **Description:** eval()
- **Evidence (Line):** `>>> filtered = qspline1d_eval(qspline1d(sig), time)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 812. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/signal/_spline_filters.py:675
- **Description:** eval()
- **Evidence (Line):** `res[cond1] = qspline1d_eval(cj, -newx[cond1])`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 813. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/signal/_spline_filters.py:676
- **Description:** eval()
- **Evidence (Line):** `res[cond2] = qspline1d_eval(cj, 2 * (N - 1) - newx[cond2])`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 814. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/signal/tests/test_bsplines.py:164
- **Description:** eval()
- **Evidence (Line):** `def test_cspline1d_eval(self, xp):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 815. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/signal/tests/test_bsplines.py:165
- **Description:** eval()
- **Evidence (Line):** `r = signal.cspline1d_eval(xp.asarray([0., 0], dtype=xp.float64),`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 816. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/signal/tests/test_bsplines.py:169
- **Description:** eval()
- **Evidence (Line):** `r = signal.cspline1d_eval(xp.asarray([1., 0, 1], dtype=xp.float64),`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 817. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/signal/tests/test_bsplines.py:174
- **Description:** eval()
- **Evidence (Line):** `r = signal.cspline1d_eval(xp.asarray([1.0, 0, 1], dtype=xp.float64),`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 818. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/signal/tests/test_bsplines.py:195
- **Description:** eval()
- **Evidence (Line):** `signal.cspline1d_eval(cj, xp.asarray(newx), dx=dx, x0=x[0]), newy`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 819. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/signal/tests/test_bsplines.py:200
- **Description:** eval()
- **Evidence (Line):** `signal.cspline1d_eval(xp.asarray([], dtype=xp.float64),`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 820. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/signal/tests/test_bsplines.py:205
- **Description:** eval()
- **Evidence (Line):** `def test_qspline1d_eval(self, xp):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 821. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/signal/tests/test_bsplines.py:206
- **Description:** eval()
- **Evidence (Line):** `xp_assert_close(signal.qspline1d_eval(xp.asarray([0., 0]), xp.asarray([0.])),`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 822. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/signal/tests/test_bsplines.py:209
- **Description:** eval()
- **Evidence (Line):** `xp_assert_equal(signal.qspline1d_eval(xp.asarray([1., 0, 1]), xp.asarray([])),`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 823. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/signal/tests/test_bsplines.py:214
- **Description:** eval()
- **Evidence (Line):** `r = signal.qspline1d_eval(xp.asarray([1.0, 0, 1], dtype=xp.float64),`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 824. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/signal/tests/test_bsplines.py:234
- **Description:** eval()
- **Evidence (Line):** `r = signal.qspline1d_eval(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 825. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/signal/tests/test_bsplines.py:241
- **Description:** eval()
- **Evidence (Line):** `signal.qspline1d_eval(xp.asarray([], dtype=xp.float64),`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 826. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/signal/tests/test_signaltools.py:1686
- **Description:** eval()
- **Evidence (Line):** `y2 = signal.cspline1d_eval(cj, x2, dx=dx, x0=x[0])`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 827. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/signal/tests/test_signaltools.py:1704
- **Description:** eval()
- **Evidence (Line):** `ynew = signal.cspline1d_eval(cy, xnew)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 828. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/sparse/csgraph/tests/test_graph_laplacian.py:43
- **Description:** eval()
- **Evidence (Line):** `mat = eval(mat, dict(np=np, sparse=sparse))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 829. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/sparse/csgraph/tests/test_graph_laplacian.py:299
- **Description:** eval()
- **Evidence (Line):** `d[L] = eval(L)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 830. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/sparse/csgraph/tests/test_graph_laplacian.py:301
- **Description:** eval()
- **Evidence (Line):** `d[L] = eval(L)(np.eye(n, dtype=mat.dtype))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 831. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/scipy/sparse/linalg/tests/test_interface.py:927
- **Description:** pickle load/dumps
- **Evidence (Line):** `B = pickle.loads(s)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 832. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/scipy/sparse/tests/test_base.py:2334
- **Description:** pickle load/dumps
- **Evidence (Line):** `sploaded = pickle.loads(pickle.dumps(datsp, protocol=protocol))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 833. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/spatial/tests/test_distance.py:424
- **Description:** eval()
- **Evidence (Line):** `cdist(X1, X2, metric=eval(metric), **kwargs)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 834. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/spatial/tests/test_distance.py:430
- **Description:** eval()
- **Evidence (Line):** `cdist(X1, X2, metric=eval(metric), *args)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 835. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/spatial/tests/test_distance.py:537
- **Description:** eval()
- **Evidence (Line):** `y2 = cdist(X1, X2, metric=eval(metric), **kwargs)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 836. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/spatial/tests/test_distance.py:547
- **Description:** eval()
- **Evidence (Line):** `cdist(X1, X2, metric=eval(metric), **kwargs)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 837. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/spatial/tests/test_distance.py:714
- **Description:** eval()
- **Evidence (Line):** `pdist(X1, metric=eval(metric), **kwargs)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 838. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/spatial/tests/test_distance.py:720
- **Description:** eval()
- **Evidence (Line):** `pdist(X1, metric=eval(metric), *args)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 839. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/spatial/tests/test_distance.py:1352
- **Description:** eval()
- **Evidence (Line):** `y2 = pdist(X, metric=eval(metric), **kwargs)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 840. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/spatial/tests/test_distance.py:1362
- **Description:** eval()
- **Evidence (Line):** `pdist(X, metric=eval(metric), **kwargs)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 841. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/spatial/tests/test_distance.py:2021
- **Description:** eval()
- **Evidence (Line):** `for m in [metric, eval(metric), "test_" + metric]:`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 842. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/scipy/spatial/tests/test_kdtree.py:911
- **Description:** pickle load/dumps
- **Evidence (Line):** `T2 = pickle.loads(tmp)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 843. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/scipy/spatial/tests/test_kdtree.py:925
- **Description:** pickle load/dumps
- **Evidence (Line):** `T2 = pickle.loads(tmp)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 844. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/scipy/spatial/transform/tests/test_rigid_transform.py:1502
- **Description:** pickle load/dumps
- **Evidence (Line):** `unpickled = pickle.loads(pkl)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 845. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/scipy/spatial/transform/tests/test_rotation.py:2611
- **Description:** pickle load/dumps
- **Evidence (Line):** `unpickled = pickle.loads(pkl)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 846. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/special/_precompute/wright_bessel.py:183
- **Description:** eval()
- **Evidence (Line):** `def eval(cls, n, rho, v):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 847. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/special/_precompute/wright_bessel.py:203
- **Description:** eval()
- **Evidence (Line):** `def eval(cls, m, rho, beta):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 848. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/special/_ufunc_tools.py:159
- **Description:** exec()
- **Evidence (Line):** `exec(code, namespace)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 849. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/special/tests/test_orthogonal.py:282
- **Description:** eval()
- **Evidence (Line):** `p = eval(pstr)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 850. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/scipy/special/tests/test_support_alternative_backends.py:326
- **Description:** pickle load/dumps
- **Evidence (Line):** `roundtrip = pickle.loads(pickle.dumps(func))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 851. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/stats/_continued_fraction.py:325
- **Description:** eval()
- **Evidence (Line):** `def pre_func_eval(work):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 852. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/stats/_continued_fraction.py:329
- **Description:** eval()
- **Evidence (Line):** `def post_func_eval(n, ab, work):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 853. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/stats/_continuous_distns.py:3482
- **Description:** eval()
- **Evidence (Line):** `def sk1_eval(c, *args):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 854. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/stats/_continuous_distns.py:3494
- **Description:** eval()
- **Evidence (Line):** `def ku1_eval(c, *args):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 855. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/stats/_distn_infrastructure.py:369
- **Description:** exec()
- **Evidence (Line):** `exec('del ' + obj)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 856. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/stats/_distn_infrastructure.py:748
- **Description:** exec()
- **Evidence (Line):** `exec(self._parse_arg_template, ns)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 857. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/scipy/stats/tests/common_tests.py:294
- **Description:** pickle load/dumps
- **Evidence (Line):** `unpickled = pickle.loads(s)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 858. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/scipy/stats/tests/common_tests.py:307
- **Description:** pickle load/dumps
- **Evidence (Line):** `unpickled = pickle.loads(pkl)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 859. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/scipy/stats/tests/common_tests.py:317
- **Description:** pickle load/dumps
- **Evidence (Line):** `unpickled_fit_function = pickle.loads(pickled_fit_function)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 860. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/scipy/stats/tests/test_axis_nan_policy.py:839
- **Description:** pickle load/dumps
- **Evidence (Line):** `unpickled_hypotest = pickle.loads(pickled_hypotest)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 861. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/stats/tests/test_continued_fraction.py:144
- **Description:** eval()
- **Evidence (Line):** `def test_feval(self, xp):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 862. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/stats/tests/test_continuous.py:87
- **Description:** eval()
- **Evidence (Line):** `ref = eval(f'(a {left_comparison} x) & (x {right_comparison} b)')`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 863. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/scipy/stats/tests/test_continuous.py:2138
- **Description:** eval()
- **Evidence (Line):** `new_dist = eval(repr(dist))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 864. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/scipy/stats/tests/test_continuous.py:994
- **Description:** pickle load/dumps
- **Evidence (Line):** `dist3 = pickle.loads(pickle.dumps(dist1))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 865. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/scipy/stats/tests/test_distributions.py:6988
- **Description:** pickle load/dumps
- **Evidence (Line):** `unpickled = pickle.loads(s)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 866. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/scipy/stats/tests/test_multivariate.py:4396
- **Description:** pickle load/dumps
- **Evidence (Line):** `unpickled = pickle.loads(s)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 867. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/scipy/stats/tests/test_sampling.py:256
- **Description:** pickle load/dumps
- **Evidence (Line):** `rng2 = pickle.loads(obj)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 868. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/six.py:740
- **Description:** exec()
- **Evidence (Line):** `exec("""exec _code_ in _globs_, _locs_""")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 869. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/sknetwork/data/load.py:159
- **Description:** pickle load/dumps
- **Evidence (Line):** `dataset[file_name] = pickle.load(f)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 870. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/sknetwork/data/load.py:222
- **Description:** pickle load/dumps
- **Evidence (Line):** `data[file_name] = pickle.load(f)`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 871. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/dialects/mssql/base.py:1857
- **Description:** exec()
- **Evidence (Line):** `def pre_exec(self):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 872. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/dialects/mssql/base.py:1918
- **Description:** exec()
- **Evidence (Line):** `def post_exec(self):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 873. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/dialects/mysql/_mariadb_shim.py:81
- **Description:** exec()
- **Evidence (Line):** `def post_exec(self) -> None:`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 874. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/dialects/mysql/mariadbconnector.py:103
- **Description:** exec()
- **Evidence (Line):** `def post_exec(self) -> None:`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 875. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/dialects/mysql/mariadbconnector.py:104
- **Description:** exec()
- **Evidence (Line):** `super().post_exec()`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 876. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/dialects/oracle/base.py:2078
- **Description:** exec()
- **Evidence (Line):** `def pre_exec(self):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 877. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/dialects/oracle/cx_oracle.py:1117
- **Description:** exec()
- **Evidence (Line):** `def pre_exec(self):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 878. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/dialects/oracle/cx_oracle.py:1118
- **Description:** exec()
- **Evidence (Line):** `super().pre_exec()`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 879. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/dialects/oracle/cx_oracle.py:1128
- **Description:** exec()
- **Evidence (Line):** `def post_exec(self):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 880. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py:483
- **Description:** exec()
- **Evidence (Line):** `def pre_exec(self):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 881. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/pg8000.py:327
- **Description:** exec()
- **Evidence (Line):** `def pre_exec(self):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 882. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/psycopg2.py:568
- **Description:** exec()
- **Evidence (Line):** `def post_exec(self):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 883. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1827
- **Description:** exec()
- **Evidence (Line):** `context.pre_exec()`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 884. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/engine/base.py:1967
- **Description:** exec()
- **Evidence (Line):** `context.post_exec()`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 885. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/engine/base.py:2134
- **Description:** exec()
- **Evidence (Line):** `context.post_exec()`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 886. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/engine/default.py:2042
- **Description:** exec()
- **Evidence (Line):** `def pre_exec(self):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 887. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/engine/default.py:2050
- **Description:** exec()
- **Evidence (Line):** `def post_exec(self):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 888. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/engine/default.py:2070
- **Description:** exec()
- **Evidence (Line):** `calculated within post_exec().`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 889. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/engine/interfaces.py:3189
- **Description:** exec()
- **Evidence (Line):** `sql.Compiled object by the time pre_exec() has completed."""`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 890. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/engine/interfaces.py:3333
- **Description:** exec()
- **Evidence (Line):** `def pre_exec(self) -> None:`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 891. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/engine/interfaces.py:3379
- **Description:** exec()
- **Evidence (Line):** `def post_exec(self) -> None:`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 892. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/ext/serializer.py:64
- **Description:** pickle load/dumps
- **Evidence (Line):** `pickle.loads()/dumps() can be used to fully dump any ``MetaData`` object,`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 893. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/ext/serializer.py:149
- **Description:** pickle load/dumps
- **Evidence (Line):** `cls = pickle.loads(b64decode(clsarg))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 894. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/ext/serializer.py:152
- **Description:** pickle load/dumps
- **Evidence (Line):** `cls = pickle.loads(b64decode(args))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 895. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/ext/serializer.py:155
- **Description:** pickle load/dumps
- **Evidence (Line):** `cls = pickle.loads(b64decode(args))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 896. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/ext/serializer.py:159
- **Description:** pickle load/dumps
- **Evidence (Line):** `cls = pickle.loads(b64decode(mapper))`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 897. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/orm/_orm_constructors.py:1323
- **Description:** eval()
- **Evidence (Line):** `registry of tables.  The Python ``eval()`` function is no longer`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 898. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/orm/_orm_constructors.py:1559
- **Description:** eval()
- **Evidence (Line):** `argument is interpreted using Python's ``eval()`` function.`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 899. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/orm/_orm_constructors.py:1763
- **Description:** eval()
- **Evidence (Line):** `argument is interpreted using Python's ``eval()`` function.`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 900. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/orm/_orm_constructors.py:1860
- **Description:** eval()
- **Evidence (Line):** `argument is interpreted using Python's ``eval()`` function.`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 901. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/orm/_orm_constructors.py:1879
- **Description:** eval()
- **Evidence (Line):** `argument is interpreted using Python's ``eval()`` function.`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 902. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/orm/_orm_constructors.py:1921
- **Description:** eval()
- **Evidence (Line):** `argument is interpreted using Python's ``eval()`` function.`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 903. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/orm/bulk_persistence.py:694
- **Description:** exec()
- **Evidence (Line):** `def orm_pre_session_exec(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 904. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/orm/bulk_persistence.py:1211
- **Description:** exec()
- **Evidence (Line):** `def orm_pre_session_exec(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 905. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/orm/clsregistry.py:592
- **Description:** eval()
- **Evidence (Line):** `x = eval(self.arg, globals(), self._dict)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 906. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/orm/context.py:295
- **Description:** exec()
- **Evidence (Line):** `def orm_pre_session_exec(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 907. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/orm/context.py:345
- **Description:** exec()
- **Evidence (Line):** `def orm_pre_session_exec(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 908. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/orm/context.py:506
- **Description:** exec()
- **Evidence (Line):** `def orm_pre_session_exec(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 909. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/orm/events.py:1986
- **Description:** exec()
- **Evidence (Line):** `def after_flush_postexec(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 910. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2287
- **Description:** exec()
- **Evidence (Line):** `) = compile_state_cls.orm_pre_session_exec(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 911. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2327
- **Description:** exec()
- **Evidence (Line):** `# now run orm_pre_session_exec() "for real".   if there were`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 912. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/orm/session.py:2336
- **Description:** exec()
- **Evidence (Line):** `) = compile_state_cls.orm_pre_session_exec(`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 913. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/orm/session.py:4674
- **Description:** exec()
- **Evidence (Line):** `self.dispatch.after_flush_postexec(self, flush_context)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 914. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/orm/strategies.py:2923
- **Description:** exec()
- **Evidence (Line):** `def load_collection_from_joined_exec(state, dict_, row):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 915. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/orm/strategies.py:2962
- **Description:** exec()
- **Evidence (Line):** `def load_scalar_from_joined_exec(state, dict_, row):`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 916. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/sql/lambdas.py:1264
- **Description:** exec()
- **Evidence (Line):** `exec(code, vars_, vars_)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 917. [Critical] Insecure Deserialization
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/sql/sqltypes.py:2034
- **Description:** pickle load/dumps
- **Evidence (Line):** ```pickle.dumps()`` to incoming objects, and ``pickle.loads()`` on`
- **Exploit Scenario:** Attacker could achieve remote code execution
- **Fix Recommendation:** Use safe serialization formats (JSON), avoid pickle/yaml.load with untrusted data
- **Confidence:** High

### 918. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/testing/plugin/pytestplugin.py:671
- **Description:** exec()
- **Evidence (Line):** `exec(code, env)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 919. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/util/langhelpers.py:455
- **Description:** exec()
- **Evidence (Line):** `exec(code, env)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 920. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/util/langhelpers.py:2163
- **Description:** exec()
- **Evidence (Line):** `exec(code, env)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 921. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/util/typing.py:265
- **Description:** eval()
- **Evidence (Line):** `annotation = eval(expression, cls_namespace, locals_)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 922. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/util/typing.py:267
- **Description:** eval()
- **Evidence (Line):** `annotation = eval(expression, base_globals, locals_)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 923. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/util/typing.py:293
- **Description:** eval()
- **Evidence (Line):** `# name only, just look in globals.  eval() works perfectly fine here,`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 924. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/tqdm/cli.py:38
- **Description:** eval()
- **Evidence (Line):** `return literal_eval(f'"{val}"').encode()`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 925. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/tqdm/cli.py:301
- **Description:** eval()
- **Evidence (Line):** `t.update(literal_eval(i.decode()))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 926. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/tqdm/cli.py:304
- **Description:** eval()
- **Evidence (Line):** `t.update(literal_eval(i.decode()) - t.n)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 927. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/tqdm/cli.py:317
- **Description:** eval()
- **Evidence (Line):** `t.update(literal_eval(i.decode()))`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 928. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/tqdm/cli.py:320
- **Description:** eval()
- **Evidence (Line):** `t.update(literal_eval(i.decode()) - t.n)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 929. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/typing_extensions.py:1591
- **Description:** eval()
- **Evidence (Line):** `(unless you are familiar with how eval() and exec() work).  The`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 930. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/typing_extensions.py:4167
- **Description:** eval()
- **Evidence (Line):** `# as a way of emulating annotation scopes when calling `eval()``
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 931. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/typing_extensions.py:4172
- **Description:** eval()
- **Evidence (Line):** `value if not isinstance(value, str) else eval(value, globals, locals)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 932. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/typing_extensions.py:4219
- **Description:** eval()
- **Evidence (Line):** `# If we pass None to eval() below, the globals of this module are used.`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 933. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/typing_extensions.py:4231
- **Description:** eval()
- **Evidence (Line):** `# as a way of emulating annotation scopes when calling `eval()``
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 934. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/typing_extensions.py:4254
- **Description:** eval()
- **Evidence (Line):** `value = eval(code, globals, locals)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 935. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/typing_extensions.py:1591
- **Description:** exec()
- **Evidence (Line):** `(unless you are familiar with how eval() and exec() work).  The`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 936. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/typing_inspection/typing_objects.py:112
- **Description:** exec()
- **Evidence (Line):** `exec(func_code, globals_, locals_)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 937. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/typing_inspection/typing_objects.py:153
- **Description:** exec()
- **Evidence (Line):** `exec(func_code, globals_, locals_)`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 938. [Critical] Command Injection
- **File:** .venv-test/lib/python3.12/site-packages/websockets/cli.py:189
- **Description:** os.system()
- **Evidence (Line):** `os.system("")`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 939. [Critical] Hardcoded Secret
- **File:** DEPLOYMENT.md:545
- **Description:** API Key Assignment detected
- **Evidence (Line):** `export DATADOG_API_KEY="your-datadog-key"`
- **Exploit Scenario:** Attacker could extract credentials and gain unauthorized access
- **Fix Recommendation:** Move secrets to environment variables or secret manager, rotate compromised credentials
- **Confidence:** High

### 940. [Critical] Hardcoded Secret
- **File:** docs/GUIDE.md:220
- **Description:** Password Assignment detected
- **Evidence (Line):** `password="your_password",`
- **Exploit Scenario:** Attacker could extract credentials and gain unauthorized access
- **Fix Recommendation:** Move secrets to environment variables or secret manager, rotate compromised credentials
- **Confidence:** High

### 941. [Critical] Command Injection
- **File:** pyvectorhound/_mcp_tools.py:257
- **Description:** eval()
- **Evidence (Line):** `async def batch_retrieval(self, index_name: str, doc_ids: List[str]) -> Dict[str, Any]:`
- **Exploit Scenario:** Attacker could execute arbitrary system commands
- **Fix Recommendation:** Avoid shell execution, use subprocess with shell=False and list args
- **Confidence:** High

### 942. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/PIL/GdImageFile.py:77
- **Description:** Django raw SQL concatenation
- **Evidence (Line):** `self.palette = ImagePalette.raw(`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 943. [High] SSRF
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/document_loaders/ifixit.py:72
- **Description:** requests with URL concatenation
- **Evidence (Line):** `res = requests.get(`
- **Exploit Scenario:** Attacker could make requests to internal services/metadata endpoints
- **Fix Recommendation:** Validate URLs against allowlist, block private IP ranges, disable redirects or validate them
- **Confidence:** Medium

### 944. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/document_loaders/oracleadb_loader.py:99
- **Description:** SQL f-string interpolation
- **Evidence (Line):** `cursor.execute(f"alter session set current_schema={self.schema}")`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 945. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/graphs/kuzu_graph.py:81
- **Description:** SQL f-string interpolation
- **Evidence (Line):** `query_result = self.conn.execute(`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 946. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/graphs/nebula_graph.py:181
- **Description:** SQL f-string interpolation
- **Evidence (Line):** `r = self.execute(f"DESCRIBE TAG `{tag_name}`")`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 947. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/graphs/nebula_graph.py:189
- **Description:** SQL f-string interpolation
- **Evidence (Line):** `r = self.execute(f"DESCRIBE EDGE `{edge_type_name}`")`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 948. [High] SSRF
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/tools/nuclia/tool.py:130
- **Description:** requests with URL concatenation
- **Evidence (Line):** `response = requests.post(`
- **Exploit Scenario:** Attacker could make requests to internal services/metadata endpoints
- **Fix Recommendation:** Validate URLs against allowlist, block private IP ranges, disable redirects or validate them
- **Confidence:** Medium

### 949. [High] SSRF
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/tools/nuclia/tool.py:154
- **Description:** requests with URL concatenation
- **Evidence (Line):** `response = requests.post(`
- **Exploit Scenario:** Attacker could make requests to internal services/metadata endpoints
- **Fix Recommendation:** Validate URLs against allowlist, block private IP ranges, disable redirects or validate them
- **Confidence:** Medium

### 950. [High] SSRF
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/tools/nuclia/tool.py:201
- **Description:** requests with URL concatenation
- **Evidence (Line):** `res = requests.get(`
- **Exploit Scenario:** Attacker could make requests to internal services/metadata endpoints
- **Fix Recommendation:** Validate URLs against allowlist, block private IP ranges, disable redirects or validate them
- **Confidence:** Medium

### 951. [High] SSRF
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/tools/zenguard/tool.py:92
- **Description:** requests with URL concatenation
- **Evidence (Line):** `response = requests.post(`
- **Exploit Scenario:** Attacker could make requests to internal services/metadata endpoints
- **Fix Recommendation:** Validate URLs against allowlist, block private IP ranges, disable redirects or validate them
- **Confidence:** Medium

### 952. [High] SSRF
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/utilities/nasa.py:21
- **Description:** requests with URL concatenation
- **Evidence (Line):** `response = requests.get(`
- **Exploit Scenario:** Attacker could make requests to internal services/metadata endpoints
- **Fix Recommendation:** Validate URLs against allowlist, block private IP ranges, disable redirects or validate them
- **Confidence:** Medium

### 953. [High] SSRF
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/utilities/nasa.py:28
- **Description:** requests with URL concatenation
- **Evidence (Line):** `response = requests.get(IMAGE_AND_VIDEO_LIBRARY_URL + "/asset/" + query)`
- **Exploit Scenario:** Attacker could make requests to internal services/metadata endpoints
- **Fix Recommendation:** Validate URLs against allowlist, block private IP ranges, disable redirects or validate them
- **Confidence:** Medium

### 954. [High] SSRF
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/utilities/nasa.py:32
- **Description:** requests with URL concatenation
- **Evidence (Line):** `response = requests.get(IMAGE_AND_VIDEO_LIBRARY_URL + "/metadata/" + query)`
- **Exploit Scenario:** Attacker could make requests to internal services/metadata endpoints
- **Fix Recommendation:** Validate URLs against allowlist, block private IP ranges, disable redirects or validate them
- **Confidence:** Medium

### 955. [High] SSRF
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/utilities/nasa.py:36
- **Description:** requests with URL concatenation
- **Evidence (Line):** `response = requests.get(IMAGE_AND_VIDEO_LIBRARY_URL + "/captions/" + query)`
- **Exploit Scenario:** Attacker could make requests to internal services/metadata endpoints
- **Fix Recommendation:** Validate URLs against allowlist, block private IP ranges, disable redirects or validate them
- **Confidence:** Medium

### 956. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/vectorstores/duckdb.py:186
- **Description:** SQL f-string interpolation
- **Evidence (Line):** `self._connection.execute(`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 957. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/vectorstores/duckdb.py:195
- **Description:** SQL f-string interpolation
- **Evidence (Line):** `self._connection.execute(`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 958. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/vectorstores/oraclevs.py:84
- **Description:** SQL f-string interpolation
- **Evidence (Line):** `cursor.execute(f"SELECT COUNT(*) FROM {table_name}")`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 959. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/vectorstores/oraclevs.py:618
- **Description:** SQL f-string interpolation
- **Evidence (Line):** `cursor.executemany(`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 960. [High] SSRF
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/vectorstores/semadb.py:77
- **Description:** requests with URL concatenation
- **Evidence (Line):** `response = requests.post(`
- **Exploit Scenario:** Attacker could make requests to internal services/metadata endpoints
- **Fix Recommendation:** Validate URLs against allowlist, block private IP ranges, disable redirects or validate them
- **Confidence:** Medium

### 961. [High] SSRF
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/vectorstores/semadb.py:86
- **Description:** requests with URL concatenation
- **Evidence (Line):** `response = requests.delete(`
- **Exploit Scenario:** Attacker could make requests to internal services/metadata endpoints
- **Fix Recommendation:** Validate URLs against allowlist, block private IP ranges, disable redirects or validate them
- **Confidence:** Medium

### 962. [High] SSRF
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/vectorstores/semadb.py:143
- **Description:** requests with URL concatenation
- **Evidence (Line):** `response = requests.post(`
- **Exploit Scenario:** Attacker could make requests to internal services/metadata endpoints
- **Fix Recommendation:** Validate URLs against allowlist, block private IP ranges, disable redirects or validate them
- **Confidence:** Medium

### 963. [High] SSRF
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/vectorstores/semadb.py:176
- **Description:** requests with URL concatenation
- **Evidence (Line):** `response = requests.delete(`
- **Exploit Scenario:** Attacker could make requests to internal services/metadata endpoints
- **Fix Recommendation:** Validate URLs against allowlist, block private IP ranges, disable redirects or validate them
- **Confidence:** Medium

### 964. [High] SSRF
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/vectorstores/semadb.py:195
- **Description:** requests with URL concatenation
- **Evidence (Line):** `response = requests.post(`
- **Exploit Scenario:** Attacker could make requests to internal services/metadata endpoints
- **Fix Recommendation:** Validate URLs against allowlist, block private IP ranges, disable redirects or validate them
- **Confidence:** Medium

### 965. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/vectorstores/sqlitevss.py:66
- **Description:** SQL f-string interpolation
- **Evidence (Line):** `self._connection.execute(`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 966. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/vectorstores/sqlitevss.py:78
- **Description:** SQL f-string interpolation
- **Evidence (Line):** `self._connection.execute(`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 967. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/vectorstores/sqlitevss.py:85
- **Description:** SQL f-string interpolation
- **Evidence (Line):** `self._connection.execute(`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 968. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/vectorstores/sqlitevss.py:110
- **Description:** SQL f-string interpolation
- **Evidence (Line):** `max_id = self._connection.execute(`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 969. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/vectorstores/sqlitevss.py:123
- **Description:** SQL f-string interpolation
- **Evidence (Line):** `self._connection.executemany(`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 970. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/vectorstores/sqlitevss.py:130
- **Description:** SQL f-string interpolation
- **Evidence (Line):** `results = self._connection.execute(`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 971. [High] .env File with Secrets
- **File:** .venv-test/lib/python3.12/site-packages/langsmith/cli/.env.example:1
- **Description:** .env.example contains potential secrets
- **Evidence (Line):** `# Don't change this file. Instead, copy it to .env and change the values there. The default values w`
- **Exploit Scenario:** Secrets in committed .env files exposed in git history
- **Fix Recommendation:** Add .env to .gitignore, remove from git history, rotate secrets
- **Confidence:** High

### 972. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/io/sql.py:2455
- **Description:** SQL f-string interpolation
- **Evidence (Line):** `self.execute(f"DELETE FROM {quoted_table_name}").close()`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 973. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/io/test_sql.py:566
- **Description:** SQL f-string interpolation
- **Evidence (Line):** `conn.execute(f"DROP TABLE IF EXISTS {sql._get_valid_sqlite_name(table_name)}")`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 974. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/io/test_sql.py:573
- **Description:** SQL f-string interpolation
- **Evidence (Line):** `cur.execute(f'DROP TABLE IF EXISTS "{table_name}"')`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 975. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/io/test_sql.py:587
- **Description:** SQL f-string interpolation
- **Evidence (Line):** `conn.execute(f"DROP VIEW IF EXISTS {sql._get_valid_sqlite_name(view_name)}")`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 976. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/io/test_sql.py:593
- **Description:** SQL f-string interpolation
- **Evidence (Line):** `cur.execute(f'DROP VIEW IF EXISTS "{view_name}"')`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 977. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/io/test_sql.py:4082
- **Description:** SQL f-string interpolation
- **Evidence (Line):** `recs = conn.execute(f"PRAGMA table_info({table})")`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 978. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/dialects/mssql/base.py:3277
- **Description:** SQL f-string interpolation
- **Evidence (Line):** `cursor.execute(f"SET TRANSACTION ISOLATION LEVEL {level}")`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 979. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/dialects/mssql/base.py:2001
- **Description:** SQL % formatting
- **Evidence (Line):** `self.cursor.execute(`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 980. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/dialects/mysql/base.py:2853
- **Description:** SQL f-string interpolation
- **Evidence (Line):** `cursor.execute(f"SET SESSION TRANSACTION ISOLATION LEVEL {level}")`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 981. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/dialects/mysql/mysqldb.py:184
- **Description:** SQL % formatting
- **Evidence (Line):** `cursor.execute("SET NAMES %s" % charset_name)`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 982. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/dialects/oracle/cx_oracle.py:1399
- **Description:** SQL f-string interpolation
- **Evidence (Line):** `cursor.execute(f"ALTER SESSION SET ISOLATION_LEVEL={level}")`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 983. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/dialects/oracle/provision.py:277
- **Description:** SQL % formatting
- **Evidence (Line):** `cursor.execute("ALTER SESSION SET CURRENT_SCHEMA=%s" % schema_name)`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 984. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/base.py:364
- **Description:** SQL % formatting
- **Evidence (Line):** `cursor.execute("SET SESSION search_path='%s'" % schema_name)`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 985. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/pg8000.py:368
- **Description:** SQL string concatenation
- **Evidence (Line):** `self.cursor.execute(`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 986. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/pg8000.py:579
- **Description:** SQL f-string interpolation
- **Evidence (Line):** `cursor.execute(f"""`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 987. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/pg8000.py:538
- **Description:** SQL % formatting
- **Evidence (Line):** `cursor.execute(`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 988. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/pg8000.py:559
- **Description:** SQL % formatting
- **Evidence (Line):** `cursor.execute(`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 989. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/dialects/postgresql/provision.py:90
- **Description:** SQL % formatting
- **Evidence (Line):** `cursor.execute("SET SESSION search_path='%s'" % schema_name)`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 990. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/dialects/sqlite/base.py:2335
- **Description:** SQL f-string interpolation
- **Evidence (Line):** `cursor.execute(f"PRAGMA read_uncommitted = {isolation_level}")`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 991. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/dialects/sqlite/provision.py:122
- **Description:** SQL f-string interpolation
- **Evidence (Line):** `dbapi_connection.execute(`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 992. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/dialects/sqlite/pysqlcipher.py:150
- **Description:** SQL f-string interpolation
- **Evidence (Line):** `cursor.execute(f"pragma key={passphrase}")`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 993. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/dialects/sqlite/pysqlcipher.py:152
- **Description:** SQL f-string interpolation
- **Evidence (Line):** `cursor.execute(f"pragma {prag}={value}")`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 994. [High] SQL Injection
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/engine/base.py:3089
- **Description:** SQL % formatting
- **Evidence (Line):** `cursor.execute("use %s" % shards[shard_id])`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 995. [High] SQL Injection
- **File:** pyvectorhound/database.py:437
- **Description:** SQL f-string interpolation
- **Evidence (Line):** `cursor.execute(f"SELECT COUNT(*) FROM `{self.index_name}`")`
- **Exploit Scenario:** Attacker could manipulate SQL queries to access/modify/delete data
- **Fix Recommendation:** Use parameterized queries/prepared statements
- **Confidence:** Medium

### 996. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/aiohttp/client.py:1357
- **Description:** SHA1 usage
- **Evidence (Line):** `match = base64.b64encode(hashlib.sha1(sec_key + WS_KEY).digest()).decode()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 997. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/aiohttp/client.py:1357
- **Description:** Weak hash algorithm
- **Evidence (Line):** `match = base64.b64encode(hashlib.sha1(sec_key + WS_KEY).digest()).decode()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 998. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/aiohttp/client_middleware_digest_auth.py:332
- **Description:** SHA1 usage
- **Evidence (Line):** `cnonce = hashlib.sha1(`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 999. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/aiohttp/client_middleware_digest_auth.py:38
- **Description:** Weak hash algorithm
- **Evidence (Line):** `"MD5": hashlib.md5,`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1000. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/aiohttp/client_middleware_digest_auth.py:39
- **Description:** Weak hash algorithm
- **Evidence (Line):** `"MD5-SESS": hashlib.md5,`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1001. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/aiohttp/client_middleware_digest_auth.py:40
- **Description:** Weak hash algorithm
- **Evidence (Line):** `"SHA": hashlib.sha1,`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1002. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/aiohttp/client_middleware_digest_auth.py:41
- **Description:** Weak hash algorithm
- **Evidence (Line):** `"SHA-SESS": hashlib.sha1,`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1003. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/aiohttp/client_middleware_digest_auth.py:332
- **Description:** Weak hash algorithm
- **Evidence (Line):** `cnonce = hashlib.sha1(`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1004. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/aiohttp/web_ws.py:338
- **Description:** SHA1 usage
- **Evidence (Line):** `hashlib.sha1(key.encode() + WS_KEY).digest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1005. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/aiohttp/web_ws.py:338
- **Description:** Weak hash algorithm
- **Evidence (Line):** `hashlib.sha1(key.encode() + WS_KEY).digest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1006. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/coverage/lcovreport.py:43
- **Description:** MD5 usage
- **Evidence (Line):** `hashed = hashlib.md5(line.encode("utf-8"), usedforsecurity=False).digest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1007. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/coverage/lcovreport.py:43
- **Description:** Weak hash algorithm
- **Evidence (Line):** `hashed = hashlib.md5(line.encode("utf-8"), usedforsecurity=False).digest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1008. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/dill/_objects.py:467
- **Description:** MD5 usage
- **Evidence (Line):** `x['HashType'] = hashlib.md5()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1009. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/dill/_objects.py:467
- **Description:** Weak hash algorithm
- **Evidence (Line):** `x['HashType'] = hashlib.md5()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1010. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/fsspec/tests/abstract/__init__.py:228
- **Description:** MD5 usage
- **Evidence (Line):** `hashed_i = md5(str(i).encode("utf-8")).hexdigest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1011. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/fsspec/tests/abstract/copy.py:548
- **Description:** MD5 usage
- **Evidence (Line):** `hashed_i = md5(str(i).encode("utf-8")).hexdigest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1012. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/fsspec/tests/abstract/get.py:576
- **Description:** MD5 usage
- **Evidence (Line):** `hashed_i = md5(str(i).encode("utf-8")).hexdigest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1013. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/fsspec/tests/abstract/put.py:582
- **Description:** MD5 usage
- **Evidence (Line):** `hashed_i = md5(str(i).encode("utf-8")).hexdigest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1014. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/fsspec/utils.py:320
- **Description:** MD5 usage
- **Evidence (Line):** `h = md5(str(args).encode())`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1015. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/fsspec/utils.py:323
- **Description:** MD5 usage
- **Evidence (Line):** `h = md5(str(args).encode(), usedforsecurity=False)`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1016. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/httpx/_auth.py:309
- **Description:** SHA1 usage
- **Evidence (Line):** `return hashlib.sha1(s).hexdigest()[:16].encode()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1017. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/httpx/_auth.py:177
- **Description:** Weak hash algorithm
- **Evidence (Line):** `"MD5": hashlib.md5,`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1018. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/httpx/_auth.py:178
- **Description:** Weak hash algorithm
- **Evidence (Line):** `"MD5-SESS": hashlib.md5,`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1019. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/httpx/_auth.py:179
- **Description:** Weak hash algorithm
- **Evidence (Line):** `"SHA": hashlib.sha1,`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1020. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/httpx/_auth.py:180
- **Description:** Weak hash algorithm
- **Evidence (Line):** `"SHA-SESS": hashlib.sha1,`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1021. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/httpx/_auth.py:309
- **Description:** Weak hash algorithm
- **Evidence (Line):** `return hashlib.sha1(s).hexdigest()[:16].encode()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1022. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/httpx2/_auth.py:300
- **Description:** SHA1 usage
- **Evidence (Line):** `return hashlib.sha1(s).hexdigest()[:16].encode()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1023. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/httpx2/_auth.py:300
- **Description:** Weak hash algorithm
- **Evidence (Line):** `return hashlib.sha1(s).hexdigest()[:16].encode()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1024. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/huggingface_hub/_local_folder.py:492
- **Description:** SHA1 usage
- **Evidence (Line):** `return base64.urlsafe_b64encode(hashlib.sha1(filename.encode()).digest()).decode()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1025. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/huggingface_hub/_local_folder.py:492
- **Description:** Weak hash algorithm
- **Evidence (Line):** `return base64.urlsafe_b64encode(hashlib.sha1(filename.encode()).digest()).decode()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1026. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/huggingface_hub/hf_file_system.py:248
- **Description:** MD5 usage
- **Evidence (Line):** `h = md5(str(tokenize_args).encode())`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1027. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/huggingface_hub/utils/insecure_hashlib.py:30
- **Description:** Weak hash algorithm
- **Evidence (Line):** `md5 = functools.partial(hashlib.md5, usedforsecurity=False)`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1028. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/huggingface_hub/utils/insecure_hashlib.py:31
- **Description:** Weak hash algorithm
- **Evidence (Line):** `sha1 = functools.partial(hashlib.sha1, usedforsecurity=False)`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1029. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/huggingface_hub/utils/sha.py:59
- **Description:** SHA1 usage
- **Evidence (Line):** `sha = sha1()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1030. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/jinja2/bccache.py:156
- **Description:** SHA1 usage
- **Evidence (Line):** `hash = sha1(name.encode("utf-8"))`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1031. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/jinja2/bccache.py:165
- **Description:** SHA1 usage
- **Evidence (Line):** `return sha1(source.encode("utf-8")).hexdigest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1032. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/jinja2/loaders.py:661
- **Description:** SHA1 usage
- **Evidence (Line):** `return "tmpl_" + sha1(name.encode("utf-8")).hexdigest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1033. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain/embeddings/cache.py:29
- **Description:** SHA1 usage
- **Evidence (Line):** `hash_value = hashlib.sha1(input_string.encode("utf-8")).hexdigest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1034. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain/embeddings/cache.py:29
- **Description:** Weak hash algorithm
- **Evidence (Line):** `hash_value = hashlib.sha1(input_string.encode("utf-8")).hexdigest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1035. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain_classic/embeddings/cache.py:38
- **Description:** SHA1 usage
- **Evidence (Line):** `sha1_hex = hashlib.sha1(text.encode("utf-8"), usedforsecurity=False).hexdigest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1036. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain_classic/embeddings/cache.py:38
- **Description:** Weak hash algorithm
- **Evidence (Line):** `sha1_hex = hashlib.sha1(text.encode("utf-8"), usedforsecurity=False).hexdigest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1037. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/cache.py:100
- **Description:** MD5 usage
- **Evidence (Line):** `return hashlib.md5(_input.encode()).hexdigest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1038. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/cache.py:1566
- **Description:** MD5 usage
- **Evidence (Line):** `prompt_md5 = self.get_md5(prompt)`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1039. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/cache.py:1584
- **Description:** MD5 usage
- **Evidence (Line):** `.where(self.cache_schema.prompt_md5 == self.get_md5(prompt))  # type: ignore`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1040. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/cache.py:1591
- **Description:** MD5 usage
- **Evidence (Line):** `prompt_pd5 = self.get_md5(prompt)`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1041. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/cache.py:1608
- **Description:** MD5 usage
- **Evidence (Line):** `def get_md5(input_string: str) -> str:`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1042. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/cache.py:1609
- **Description:** MD5 usage
- **Evidence (Line):** `return hashlib.md5(input_string.encode()).hexdigest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1043. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/cache.py:100
- **Description:** Weak hash algorithm
- **Evidence (Line):** `return hashlib.md5(_input.encode()).hexdigest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1044. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/cache.py:1609
- **Description:** Weak hash algorithm
- **Evidence (Line):** `return hashlib.md5(input_string.encode()).hexdigest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1045. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/callbacks/utils.py:74
- **Description:** SHA1 usage
- **Evidence (Line):** `return hashlib.sha1(s.encode("utf-8")).hexdigest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1046. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/callbacks/utils.py:74
- **Description:** Weak hash algorithm
- **Evidence (Line):** `return hashlib.sha1(s.encode("utf-8")).hexdigest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1047. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/document_loaders/docugami.py:131
- **Description:** MD5 usage
- **Evidence (Line):** `_hashed_id = hashlib.md5(dg_chunk.text.encode()).hexdigest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1048. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/document_loaders/docugami.py:131
- **Description:** Weak hash algorithm
- **Evidence (Line):** `_hashed_id = hashlib.md5(dg_chunk.text.encode()).hexdigest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1049. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/document_loaders/evernote.py:92
- **Description:** MD5 usage
- **Evidence (Line):** `rsc_dict["hash"] = hashlib.md5(rsc_dict[elem.tag]).hexdigest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1050. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/document_loaders/evernote.py:92
- **Description:** Weak hash algorithm
- **Evidence (Line):** `rsc_dict["hash"] = hashlib.md5(rsc_dict[elem.tag]).hexdigest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1051. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/graphs/age_graph.py:714
- **Description:** MD5 usage
- **Evidence (Line):** `doc.source.metadata["id"] = md5(`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1052. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/graphs/gremlin_graph.py:129
- **Description:** MD5 usage
- **Evidence (Line):** `doc_id = hashlib.md5(document.source.page_content.encode()).hexdigest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1053. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/graphs/gremlin_graph.py:129
- **Description:** Weak hash algorithm
- **Evidence (Line):** `doc_id = hashlib.md5(document.source.page_content.encode()).hexdigest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1054. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/graphs/neo4j_graph.py:595
- **Description:** MD5 usage
- **Evidence (Line):** `document.source.metadata["id"] = md5(`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1055. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/tools/databricks/tool.py:76
- **Description:** MD5 usage
- **Evidence (Line):** `type_hash = md5(uc_type_json_str.encode()).hexdigest()[:8]`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1056. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/vectorstores/alibabacloud_opensearch.py:183
- **Description:** SHA1 usage
- **Evidence (Line):** `id_list = [sha1(t.encode("utf-8")).hexdigest() for t in texts]`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1057. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/vectorstores/alibabacloud_opensearch.py:418
- **Description:** SHA1 usage
- **Evidence (Line):** `id_list = [sha1(t.encode("utf-8")).hexdigest() for t in texts]`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1058. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/vectorstores/apache_doris.py:210
- **Description:** SHA1 usage
- **Evidence (Line):** `ids = ids or [sha1(t.encode("utf-8")).hexdigest() for t in texts]`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1059. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/vectorstores/clickhouse.py:451
- **Description:** SHA1 usage
- **Evidence (Line):** `ids = ids or [sha1(t.encode("utf-8")).hexdigest() for t in texts]`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1060. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/vectorstores/manticore_search.py:210
- **Description:** SHA1 usage
- **Evidence (Line):** `str(int(sha1(t.encode("utf-8")).hexdigest()[:15], 16))`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1061. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/vectorstores/myscale.py:243
- **Description:** SHA1 usage
- **Evidence (Line):** `ids = ids or [sha1(t.encode("utf-8")).hexdigest() for t in texts]`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1062. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/vectorstores/neo4j_vector.py:792
- **Description:** MD5 usage
- **Evidence (Line):** `ids = [md5(text.encode("utf-8")).hexdigest() for text in texts]`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1063. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/vectorstores/neo4j_vector.py:867
- **Description:** MD5 usage
- **Evidence (Line):** `ids = [md5(text.encode("utf-8")).hexdigest() for text in texts]`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1064. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/vectorstores/starrocks.py:263
- **Description:** SHA1 usage
- **Evidence (Line):** `ids = ids or [sha1(t.encode("utf-8")).hexdigest() for t in texts]`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1065. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/vectorstores/vectara.py:383
- **Description:** MD5 usage
- **Evidence (Line):** `doc_hash = md5()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1066. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/vectorstores/yellowbrick.py:510
- **Description:** SHA1 usage
- **Evidence (Line):** `hash_object = hashlib.sha1(vector_str.encode())`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1067. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain_community/vectorstores/yellowbrick.py:510
- **Description:** Weak hash algorithm
- **Evidence (Line):** `hash_object = hashlib.sha1(vector_str.encode())`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1068. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain_core/indexing/api.py:45
- **Description:** SHA1 usage
- **Evidence (Line):** `hash_value = hashlib.sha1(input_string.encode("utf-8")).hexdigest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1069. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain_core/indexing/api.py:52
- **Description:** SHA1 usage
- **Evidence (Line):** `hash_value = hashlib.sha1(serialized_data.encode("utf-8")).hexdigest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1070. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain_core/indexing/api.py:45
- **Description:** Weak hash algorithm
- **Evidence (Line):** `hash_value = hashlib.sha1(input_string.encode("utf-8")).hexdigest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1071. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langchain_core/indexing/api.py:52
- **Description:** Weak hash algorithm
- **Evidence (Line):** `hash_value = hashlib.sha1(serialized_data.encode("utf-8")).hexdigest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1072. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/langgraph/pregel/_algo.py:1397
- **Description:** SHA1 usage
- **Evidence (Line):** `sha = sha1(namespace, usedforsecurity=False)`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1073. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/pandas/tests/io/pytables/test_store.py:65
- **Description:** Weak hash algorithm
- **Evidence (Line):** `def checksum(filename, hash_factory=hashlib.md5, chunk_num_blocks=128):`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1074. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/requests/auth.py:179
- **Description:** MD5 usage
- **Evidence (Line):** `return hashlib.md5(x, usedforsecurity=False).hexdigest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1075. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/requests/auth.py:187
- **Description:** SHA1 usage
- **Evidence (Line):** `return hashlib.sha1(x, usedforsecurity=False).hexdigest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1076. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/requests/auth.py:237
- **Description:** SHA1 usage
- **Evidence (Line):** `cnonce = hashlib.sha1(s, usedforsecurity=False).hexdigest()[:16]`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1077. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/requests/auth.py:179
- **Description:** Weak hash algorithm
- **Evidence (Line):** `return hashlib.md5(x, usedforsecurity=False).hexdigest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1078. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/requests/auth.py:187
- **Description:** Weak hash algorithm
- **Evidence (Line):** `return hashlib.sha1(x, usedforsecurity=False).hexdigest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1079. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/requests/auth.py:237
- **Description:** Weak hash algorithm
- **Evidence (Line):** `cnonce = hashlib.sha1(s, usedforsecurity=False).hexdigest()[:16]`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1080. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/rich/tree.py:18
- **Description:** DES usage
- **Evidence (Line):** `ASCII_GUIDES (GuideType): Guide lines used when Console.ascii_only is True.`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1081. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/rich/tree.py:19
- **Description:** DES usage
- **Evidence (Line):** `TREE_GUIDES (List[GuideType, GuideType, GuideType]): Default guide lines.`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1082. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/dialects/mysql/base.py:497
- **Description:** MD5 usage
- **Evidence (Line):** `table.select(table.c.password == func.md5("plaintext"))`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1083. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/testing/plugin/pytestplugin.py:561
- **Description:** MD5 usage
- **Evidence (Line):** `digest = hashlib.md5(`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1084. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/testing/plugin/pytestplugin.py:561
- **Description:** Weak hash algorithm
- **Evidence (Line):** `digest = hashlib.md5(`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1085. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/util/compat.py:138
- **Description:** MD5 usage
- **Evidence (Line):** `return hashlib.md5(usedforsecurity=False)`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1086. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/sqlalchemy/util/compat.py:138
- **Description:** Weak hash algorithm
- **Evidence (Line):** `return hashlib.md5(usedforsecurity=False)`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1087. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/tiktoken/load.py:51
- **Description:** SHA1 usage
- **Evidence (Line):** `cache_key = hashlib.sha1(blobpath.encode()).hexdigest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1088. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/tiktoken/load.py:51
- **Description:** Weak hash algorithm
- **Evidence (Line):** `cache_key = hashlib.sha1(blobpath.encode()).hexdigest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1089. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/websockets/utils.py:34
- **Description:** SHA1 usage
- **Evidence (Line):** `sha1 = hashlib.sha1((key + GUID).encode()).digest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High

### 1090. [Medium] Weak Cryptography
- **File:** .venv-test/lib/python3.12/site-packages/websockets/utils.py:34
- **Description:** Weak hash algorithm
- **Evidence (Line):** `sha1 = hashlib.sha1((key + GUID).encode()).digest()`
- **Exploit Scenario:** Weak algorithms vulnerable to collision/brute force attacks
- **Fix Recommendation:** Use modern algorithms (SHA-256+, bcrypt/argon2 for passwords, secrets module for tokens)
- **Confidence:** High
