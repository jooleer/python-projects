#include <stdio.h>
#include <stdlib.h>
#include <string.h>
// #include <unistd.h>
// #include <io.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <dirent.h>
#include <openssl/sha.h>

int main(int argc, char *argv[])
{
  // Check the number of arguments
  if (argc != 3)
  {
    printf("Usage: %s <folder1> <folder2>\n", argv[0]);
    exit(1);
  }

  // Get the file names in the first folder
  DIR *dir1 = opendir(argv[1]);
  if (dir1 == NULL)
  {
    printf("Error opening directory %s\n", argv[1]);
    exit(1);
  }
  struct dirent *entry;
  while ((entry = readdir(dir1)) != NULL)
  {
    // Skip hidden files
    if (entry->d_name[0] == '.')
    {
      continue;
    }

    // Get the file path
    char path1[256];
    snprintf(path1, sizeof(path1), "%s/%s", argv[1], entry->d_name);

    // Get the file hash
    unsigned char hash[SHA_DIGEST_LENGTH];
    SHA1(path1, strlen(path1), hash);

    // Check if the file exists in the second folder
    DIR *dir2 = opendir(argv[2]);
    if (dir2 == NULL)
    {
      printf("Error opening directory %s\n", argv[2]);
      exit(1);
    }
    struct dirent *entry2;
    while ((entry2 = readdir(dir2)) != NULL)
    {
      // Skip hidden files
      if (entry2->d_name[0] == '.')
      {
        continue;
      }

      // Get the file path
      char path2[256];
      snprintf(path2, sizeof(path2), "%s/%s", argv[2], entry2->d_name);

      // Check if the file hashes match
      if (memcmp(hash, SHA1(path2, strlen(path2)), SHA_DIGEST_LENGTH) != 0)
      {
        printf("File %s has different hashes\n", path1);
        exit(1);
      }
    }
    closedir(dir2);
  }
  closedir(dir1);

  // All files have the same hash
  printf("All files have the same hash\n");
  return 0;
}