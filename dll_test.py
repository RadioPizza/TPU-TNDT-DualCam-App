import pefile

def list_exports_with_pefile(dll_path):
    try:
        pe = pefile.PE(dll_path)
        exports = []
        if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
            for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
                if exp.name:
                    exports.append(exp.name.decode())
        return sorted(exports)
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

# Использование
exports = list_exports_with_pefile(r'.\libirimager.dll')
for i, func_name in enumerate(exports, 1):
    print(f"{i:3}. {func_name}")