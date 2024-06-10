from typing import Union, List
from pyspark.dbutils import DBUtils

class DatabricksFilesystem:
    def __init__(self, dbutils: DBUtils) -> None:
        self.dbutils = dbutils

    def __get_filesystem_content(self, filesystem_path: str, recursive_flag: bool = True) -> list:
        '''
        This function returns paths of directories and files for the passed file system directory
        It is a private function which can be accessed only by this class functions.

        Function parameters:
        @param: filesystem_path (str): Specify the file system path for directory listing.
        @param: recursive_flag (bool - Optional (Default: True)): When set to True, this flag enables recursive listing of the file system path, including all subdirectories.
        
        Function return value
        @return: list: List of files and directory is returned
        '''
        if recursive_flag:
            dir_paths = self.dbutils.fs.ls(filesystem_path)
            subdir_paths = [self.__get_filesystem_content(p.path) for p in dir_paths if p.isDir() and p.path != filesystem_path]
            flat_subdir_paths = [p for subdir in subdir_paths for p in subdir]
            return list(map(lambda p: p.path, dir_paths)) + flat_subdir_paths
        else:
            dir_paths = self.dbutils.fs.ls(filesystem_path)
            return list(map(lambda p: p.path, dir_paths))

    def filesystem_list(self, filesystem_path: str, recursive_flag: bool = True, list_directories: bool = True, list_files: bool = True, files_starts_with: Union[str, List[str]] = None, files_ends_with: Union[str, List[str]] = None, skip_files_starts_with: Union[str, List[str]] = None, skip_files_ends_with: Union[str, List[str]] = None, case_sensitive_comparison: bool = True, sorted_output: bool = True) -> list:
        '''
        This function provides support for the missing file system operations from Databricks. These missing operations include:
            - Recursively listing directory contents
            - Listing files matching specified start and end patterns
            - Performing case-sensitive or case-insensitive file pattern matches
            - Listing only directories or only files or both
            - Generating sorted output of listing

        Function parameters:
        @param: filesystem_path (str): Specify the file system path for directory listing.
        @param: recursive_flag (bool - Optional (Default: True)): When set to True, this flag enables recursive listing of the file system path, including all subdirectories.
        @param: list_directories (bool - Optional (Default: True)): When set to True, this determines whether directories will be included in the output. If enabled, directories will be listed in the output.
        @param: list_files (bool - Optional (Default: True)): When set to True, this determines whether files will be included in the output. If enabled, files will be listed in the output.
        @param: files_starts_with (str or List[str] - Optional (Default: None)): The provided pattern or list of patterns dictates that only files starting with it will be listed in the output. This parameter operates exclusively when the "list_files" parameter is set to True, ensuring selective listing based on the specified pattern or list of patterns.
        @param: files_ends_with (str or List[str] - Optional (Default: None)): The provided pattern or list of patterns dictates that only files ending with it will be listed in the output. This parameter operates exclusively when the "list_files" parameter is set to True, ensuring selective listing based on the specified pattern or list of patterns.
        @param: skip_files_starts_with (str or List[str] - Optional (Default: None)): The provided pattern or list of patterns dictates that files starting with it will be excluded in the output. This parameter operates exclusively when the "list_files" parameter is set to True, ensuring selective listing based on the specified pattern or list of patterns.
        @param: skip_files_ends_with (str or List[str] - Optional (Default: None)): The provided pattern or list of patterns dictates that files ending with it will be excluded in the output. This parameter operates exclusively when the "list_files" parameter is set to True, ensuring selective listing based on the specified pattern or list of patterns.
        @param: case_sensitive_comparison (bool - Optional (Default: True)): When set to True, this parameter determines whether case-sensitive comparison will be applied for file pattern matching. It only functions when the "list_files" parameter is True and values are provided for either "files_starts_with" or "files_ends_with", or both.
        @param: sorted_output (bool - Optional (Default: True)): When set to True, this parameter determines whether the output will be sorted. If enabled, the output will be returned in a sorted manner, facilitating easier navigation and analysis of the results.

        Function return value
        @return: list: List of files and directory is returned
        '''
        # Set empty output
        output_paths = []

        # Get file system content
        paths = self.__get_filesystem_content(filesystem_path, recursive_flag)

        # Check if files_starts_with is a single string then convert it to a list
        if files_starts_with:
            if type(files_starts_with) is str :
                files_starts_with = [files_starts_with]

        # Check if files_ends_with is a single string then convert it to a list
        if files_ends_with:
            if type(files_ends_with) is str :
                files_ends_with = [files_ends_with]

        # Check if skip_files_starts_with is a single string then convert it to a list
        if skip_files_starts_with:
            if type(skip_files_starts_with) is str :
                skip_files_starts_with = [skip_files_starts_with]

        # Check if skip_files_ends_with is a single string then convert it to a list
        if skip_files_ends_with:
            if type(skip_files_ends_with) is str :
                skip_files_ends_with = [skip_files_ends_with]

        # If case sensitive comparision is False (i.e case insensitive comparision) then change all files_starts_with and files_ends_with strings to upper case
        if not case_sensitive_comparison:
            if files_starts_with:
                files_starts_with = [pattern.upper() for pattern in files_starts_with]
            
            if files_ends_with:
                files_ends_with = [pattern.upper() for pattern in files_ends_with]

            if skip_files_starts_with:
                skip_files_starts_with = [pattern.upper() for pattern in skip_files_starts_with]
            
            if skip_files_ends_with:
                skip_files_ends_with = [pattern.upper() for pattern in skip_files_ends_with]
     
        # Iterate over each path from the file system to decide whether it should be returned or not
        for path in paths:
            add_path = False

            # Check if the current path is directory or not
            if path[-1] == "/":
                if list_directories:
                    add_path = True
            else:
                if list_files:
                    file_start_matching = False
                    file_end_matching = False

                    # Get file name from the path
                    file_name = path.split("/")[-1]
                    
                    # Perfrom file starts with pattern match
                    if files_starts_with:
                        if case_sensitive_comparison:
                            for pattern in files_starts_with:
                                if file_name.startswith(pattern):
                                    file_start_matching = True
                                    break
                        else:
                            for pattern in files_starts_with:
                                if file_name.upper().startswith(pattern):
                                    file_start_matching = True
                                    break

                    # Perfrom file ends with pattern match
                    if files_ends_with:
                        if case_sensitive_comparison:
                            for pattern in files_ends_with:
                                if file_name.endswith(pattern):
                                    file_end_matching = True
                                    break
                        else:
                            for pattern in files_ends_with:
                                if file_name.upper().endswith(pattern):
                                    file_end_matching = True
                                    break

                    if files_starts_with and files_ends_with:
                        if file_start_matching and file_end_matching:
                            add_path = True
                    # If both files_starts_with and files_ends_with are not provided then include file
                    elif (not files_starts_with) and (not files_ends_with):
                        add_path = True
                    else:
                        if file_start_matching or file_end_matching:
                            add_path = True

                    # Check if file is to be added in the output then apply skip filters on it
                    if add_path:
                        # Perfrom skip file starts with pattern match
                        if skip_files_starts_with:
                            if case_sensitive_comparison:
                                for pattern in skip_files_starts_with:
                                    if file_name.startswith(pattern):
                                        add_path = False
                                        break
                            else:
                                for pattern in skip_files_starts_with:
                                    if file_name.upper().startswith(pattern):
                                        add_path = False
                                        break

                        # Perfrom skip file ends with pattern match
                        if skip_files_ends_with:
                            if case_sensitive_comparison:
                                for pattern in skip_files_ends_with:
                                    if file_name.endswith(pattern):
                                        add_path = False
                                        break
                            else:
                                for pattern in skip_files_ends_with:
                                    if file_name.upper().endswith(pattern):
                                        add_path = False
                                        break

            # Check if file should be added to the output or not
            if add_path:
                output_paths.append(path)

        # Return sorted or unsorted output based on sorted_output (param)
        if sorted_output:
            return sorted(output_paths)
        else:
            return output_paths