#include <stdio.h>
#include <windows.h>
#include <psapi.h>

int listDlls() {
  // Get a handle to the current process
  HANDLE hProcess = GetCurrentProcess();
  if (hProcess == NULL) {
    printf("Failed to get current process handle.\n");
    return 1;
  }

  // Array to hold the module handles
  HMODULE hMods[1024];
  DWORD cbNeeded;

  // Get the list of all modules in the current process
  if (EnumProcessModules(hProcess, hMods, sizeof(hMods), &cbNeeded)) {
    printf("Loaded DLLs:\n");
    for (unsigned int i = 0; i < (cbNeeded / sizeof(HMODULE)); i++) {
      char szModName[MAX_PATH];
      // Get the full path to the module's file
      if (GetModuleFileNameExA(hProcess, hMods[i], szModName,
                               sizeof(szModName) / sizeof(char))) {
        printf("\t%s\n", szModName);
      }
    }
  } else {
    printf("Failed to enumerate modules.\n");
    CloseHandle(hProcess);
    return 1;
  }

  // Clean up
  CloseHandle(hProcess);
  return 0;
}

int main() {
  printf("Hello World!\n");
  printf("Size of pointer is %llu.\n", sizeof(size_t));
  return listDlls();
}
