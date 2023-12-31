import pytest
import os
import tempfile
import zipfile
import time

import mf

def test_getSubdirectoriesFromDirectory():
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a subdirectory in the temporary directory
        sub_dir_path = os.path.join(temp_dir, 'subdir')
        os.mkdir(sub_dir_path)

        # Test getSubdirectoriesFromDirectory
        subdirs = mf.getSubdirectoriesFromDirectory(temp_dir)
        assert subdirs == [sub_dir_path]

def test_splitFileFromExtension():
    # Case 1: Normal case with file and extension
    file_name, extension = mf.splitFileFromExtension("test.txt")
    assert file_name == "test"
    assert extension == ".txt"

    # Case 2: File with no extension
    file_name, extension = mf.splitFileFromExtension("test")
    assert file_name == "test"
    assert extension == ""

    # Case 3: File with multiple dots in the name
    file_name, extension = mf.splitFileFromExtension("my.test.file.txt")
    assert file_name == "my.test.file"
    assert extension == ".txt"

    # Case 4: Empty string
    file_name, extension = mf.splitFileFromExtension("")
    assert file_name == ""
    assert extension == ""

def test_splitDirectoryFromFile():
    # Case 1: Normal case with directory and file
    directory, file_name = mf.splitDirectoryFromFile("/home/user/test.txt")
    assert directory == "/home/user"
    assert file_name == "test.txt"

    # Case 2: File at root directory
    directory, file_name = mf.splitDirectoryFromFile("/test.txt")
    assert directory == "/"
    assert file_name == "test.txt"

    # Case 3: File in nested directories
    directory, file_name = mf.splitDirectoryFromFile("/home/user/documents/test.txt")
    assert directory == "/home/user/documents"
    assert file_name == "test.txt"

    # Case 4: File with no directory
    directory, file_name = mf.splitDirectoryFromFile("test.txt")
    assert directory == ""
    assert file_name == "test.txt"

    # Case 5: Empty string
    directory, file_name = mf.splitDirectoryFromFile("")
    assert directory == ""
    assert file_name == ""

def test_decompressFile():
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a zip file in the temporary directory
        zip_path = os.path.join(temp_dir, 'test.zip')
        with zipfile.ZipFile(zip_path, 'w') as zip_file:
            zip_file.writestr('test.txt', 'test')
        
        # Test decompressFile
        output_path = os.path.join(temp_dir, 'output')
        os.mkdir(output_path)
        mf.decompressFile(zip_path, output_path)

        # Check if the decompression was successful
        assert os.path.isfile(os.path.join(output_path, 'test.txt'))

        # Add tests for other file types as required

def test_createFile():
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Test createFile
        file_path = os.path.join(temp_dir, 'test.txt')
        assert mf.createFile(file_path)

        # Check if the file was created
        assert os.path.isfile(file_path)

        # Test createFile with overwrite=False
        assert not mf.createFile(file_path, overwrite=False)

def test_move():
    with tempfile.TemporaryDirectory() as temp_dir:
        src_path = os.path.join(temp_dir, 'src.txt')
        dest_dir = os.path.join(temp_dir, 'dest')
        
        # Create source file
        with open(src_path, 'w') as f:
            f.write('test')

        # Test move
        mf.move(src_path, dest_dir)

        # Check if the source file is moved
        assert not os.path.isfile(src_path)
        assert os.path.isfile(os.path.join(dest_dir, 'src.txt'))

def test_delete():
    # Test 1: Standard file deletion
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, 'test.txt')
        with open(file_path, 'w') as f:
            f.write('test')
        mf.delete(file_path)
        assert not os.path.isfile(file_path)

    # Test 2: Deleting a non-existent file
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, 'test.txt')
        assert not mf.delete(file_path)

    # Test 3: Attempt to delete non-empty directory without force
    with tempfile.TemporaryDirectory() as temp_dir:
        dir_path = os.path.join(temp_dir, 'test_dir')
        os.mkdir(dir_path)
        file_in_dir_path = os.path.join(dir_path, 'test2.txt')
        with open(file_in_dir_path, 'w') as f:
            f.write('test')
        assert not mf.delete(dir_path, force=False)
        assert os.path.isdir(dir_path)

    # Test 3a: Attempt to delete non-empty directory with force
    with tempfile.TemporaryDirectory() as temp_dir:
        dir_path = os.path.join(temp_dir, 'test_dir')
        os.mkdir(dir_path)
        file_in_dir_path = os.path.join(dir_path, 'test2.txt')
        with open(file_in_dir_path, 'w') as f:
            f.write('test')
        assert mf.delete(dir_path, force=True)
        assert not os.path.isdir(dir_path)

    # Test 4: Delete file in directory then directory
    with tempfile.TemporaryDirectory() as temp_dir:
        dir_path = os.path.join(temp_dir, 'test_dir')
        os.mkdir(dir_path)
        file_in_dir_path = os.path.join(dir_path, 'test2.txt')
        with open(file_in_dir_path, 'w') as f:
            f.write('test')
        mf.delete(file_in_dir_path)
        assert mf.delete(dir_path)
        assert not os.path.isdir(dir_path)

    # Test 5: Attempt to delete directory with nested directories without force
    with tempfile.TemporaryDirectory() as temp_dir:
        dir_path = os.path.join(temp_dir, 'test_dir')
        nested_dir_path = os.path.join(dir_path, 'nested_dir')
        os.makedirs(nested_dir_path)
        assert not mf.delete(dir_path, force=False)
        assert os.path.isdir(dir_path)

    # Test 5a: Attempt to delete directory with nested directories with force
    with tempfile.TemporaryDirectory() as temp_dir:
        dir_path = os.path.join(temp_dir, 'test_dir')
        nested_dir_path = os.path.join(dir_path, 'nested_dir')
        os.makedirs(nested_dir_path)
        assert mf.delete(dir_path, force=True)
        assert not os.path.isdir(dir_path)

    # Test 6: Deleting nested directories
    with tempfile.TemporaryDirectory() as temp_dir:
        dir_path = os.path.join(temp_dir, 'test_dir')
        nested_dir_path = os.path.join(dir_path, 'nested_dir')
        os.makedirs(nested_dir_path)
        mf.delete(nested_dir_path)
        assert mf.delete(dir_path)
        assert not os.path.isdir(dir_path)


def test_copy():
    with tempfile.TemporaryDirectory() as temp_dir:
        src_path = os.path.join(temp_dir, 'src.txt')
        dest_dir = os.path.join(temp_dir, 'dest')

        # Create source file
        with open(src_path, 'w') as f:
            f.write('test')

        # Test copy
        mf.copy(src_path, dest_dir)

        # Check if the file is copied
        assert os.path.isfile(src_path)
        assert os.path.isfile(os.path.join(dest_dir, 'src.txt'))

        # Test copy with replace=True
        with open(src_path, 'w') as f:
            f.write('test2')
        mf.copy(src_path, dest_dir, replace=True)
        with open(os.path.join(dest_dir, 'src.txt'), 'r') as f:
            assert f.read() == 'test2'

def test_createDirectory():
    with tempfile.TemporaryDirectory() as temp_dir:
        dir_path = os.path.join(temp_dir, 'test')

        # Test createDirectory
        new_dir, _ = mf.createDirectory(dir_path)

        # Check if the directory is created
        assert os.path.isdir(new_dir)

def test_removeDuplicates():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create duplicate files
        file_path1 = os.path.join(temp_dir, 'test1.txt')
        file_path2 = os.path.join(temp_dir, 'test2.txt')
        with open(file_path1, 'w') as f:
            f.write('test')
        with open(file_path2, 'w') as f:
            f.write('test')

        # Test removeDuplicates
        count = mf.removeDuplicates(temp_dir)

        # Check if one duplicate file is removed
        assert count == 1
        assert os.path.isfile(file_path1) != os.path.isfile(file_path2)

def test_getMatchingTextFile():
    # Test 1: Standard Image file
    image_path = '/path/to/image.jpg'
    matching_file = mf.getMatchingTextFile(image_path)
    assert matching_file == '/path/to/image.txt'

    # Test 2: Image file with capitalized extension
    image_path = '/path/to/image.JPG'
    matching_file = mf.getMatchingTextFile(image_path)
    assert matching_file == '/path/to/image.txt'

    # Test 3: Image file without extension
    image_path = '/path/to/image'
    with pytest.raises(ValueError):
        mf.getMatchingTextFile(image_path)

    # Test 4: Non-image file
    image_path = '/path/to/text.txt'
    matching_file = mf.getMatchingTextFile(image_path)
    assert matching_file == '/path/to/text.txt'

    # Test 5: Image file with non-standard extension
    image_path = '/path/to/image.xyz'
    matching_file = mf.getMatchingTextFile(image_path)
    assert matching_file == '/path/to/image.txt'


def test_removeMatchingImage():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a text file
        txt_path = os.path.join(temp_dir, 'test.txt')
        with open(txt_path, 'w') as f:
            f.write('test')

        # Test 1: Single matching image file
        img_path = os.path.join(temp_dir, 'test.jpg')
        with open(img_path, 'w') as f:
            f.write('test')
        removed = mf.removeMatchingImage(txt_path)
        assert removed == ['test.jpg']
        assert not os.path.isfile(img_path)

        # Test 2: Multiple matching image files
        img_path1 = os.path.join(temp_dir, 'test.jpg')
        img_path2 = os.path.join(temp_dir, 'test.png')
        with open(img_path1, 'w') as f:
            f.write('test')
        with open(img_path2, 'w') as f:
            f.write('test')
        removed = mf.removeMatchingImage(txt_path)
        assert set(removed) == set(['test.jpg', 'test.png'])
        assert not os.path.isfile(img_path1)
        assert not os.path.isfile(img_path2)

        # Test 3: Non-matching image file
        img_path3 = os.path.join(temp_dir, 'test2.jpg')
        with open(img_path3, 'w') as f:
            f.write('test')
        removed = mf.removeMatchingImage(txt_path)
        assert removed == []
        assert os.path.isfile(img_path3)

        # Test 4: Nested directory structure
        nested_dir = os.path.join(temp_dir, 'nested')
        os.makedirs(nested_dir)
        img_path4 = os.path.join(nested_dir, 'test.jpg')
        with open(img_path4, 'w') as f:
            f.write('test')
        removed = mf.removeMatchingImage(txt_path)
        assert removed == []
        assert os.path.isfile(img_path4)

        # Test 5: Mixed case filenames and extensions
        img_path5 = os.path.join(temp_dir, 'TEST.JPG')
        with open(img_path5, 'w') as f:
            f.write('test')
        removed = mf.removeMatchingImage(txt_path)
        assert removed == ['TEST.JPG']
        assert not os.path.isfile(img_path5)

        # Test 6: Text file doesn't exist
        with pytest.raises(FileNotFoundError):
            mf.removeMatchingImage(os.path.join(temp_dir, 'nonexistent.txt'))


def test_empty_directory():
    with tempfile.TemporaryDirectory() as tempdir:
        # Test 1: Normal directory
        open(os.path.join(tempdir, 'tempfile'), 'w').close()
        assert mf.emptyDirectory(tempdir) == True
        assert len(os.listdir(tempdir)) == 0

        # Test 2: Directory containing subdirectories, without removing subdirs
        subdir = os.path.join(tempdir, 'subdir')
        os.mkdir(subdir)
        open(os.path.join(subdir, 'tempfile'), 'w').close()
        assert mf.emptyDirectory(tempdir) == True
        assert len(os.listdir(tempdir)) == 1

        # Test 3: Directory containing subdirectories, with removing subdirs
        subdir2 = os.path.join(tempdir, 'subdir2')
        os.mkdir(subdir2)
        open(os.path.join(subdir2, 'tempfile'), 'w').close()
        assert mf.emptyDirectory(tempdir, remove_subdirs=True) == True
        assert len(os.listdir(tempdir)) == 0

    # Test 4: Non-existent directory
    non_existent_dir = "/path/to/non/existent/directory"
    assert mf.emptyDirectory(non_existent_dir) == False

    # Test 5: Invalid path (e.g., a file instead of a directory)
    with tempfile.NamedTemporaryFile() as temp_file:
        assert mf.emptyDirectory(temp_file.name) == False

# def test_getNewestFile():
#     # Test 1: Standard get newest file
#     with tempfile.TemporaryDirectory() as temp_dir:
#         file_path1 = os.path.join(temp_dir, 'test1.txt')
#         with open(file_path1, 'w') as f:
#             f.write('test1')
#         time.sleep(2)
#         file_path2 = os.path.join(temp_dir, 'test2.txt')
#         with open(file_path2, 'w') as f:
#             f.write('test2')
#         assert mf.getNewestFile(temp_dir, ['txt']) == file_path2

#     # Test 2: Get newest file with recursive=False
#     with tempfile.TemporaryDirectory() as temp_dir:
#         subdir = os.path.join(temp_dir, 'subdir')
#         os.mkdir(subdir)
#         file_path1 = os.path.join(temp_dir, 'test1.txt')
#         with open(file_path1, 'w') as f:
#             f.write('test1')
#         time.sleep(2)
#         file_path2 = os.path.join(subdir, 'test2.txt')
#         with open(file_path2, 'w') as f:
#             f.write('test2')
#         assert mf.getNewestFile(temp_dir, ['txt'], recursive=False) == file_path1

#     # Test 3: Get newest file with startlevel and endlevel
#     with tempfile.TemporaryDirectory() as temp_dir:
#         subdir1 = os.path.join(temp_dir, 'subdir1')
#         os.mkdir(subdir1)
#         subdir2 = os.path.join(subdir1, 'subdir2')
#         os.mkdir(subdir2)
#         file_path1 = os.path.join(temp_dir, 'test1.txt')
#         with open(file_path1, 'w') as f:
#             f.write('test1')
#         time.sleep(2)
#         file_path2 = os.path.join(subdir1, 'test2.txt')
#         with open(file_path2, 'w') as f:
#             f.write('test2')
#         time.sleep(2)
#         file_path3 = os.path.join(subdir2, 'test3.txt')
#         with open(file_path3, 'w') as f:
#             f.write('test3')
#         assert mf.getNewestFile(temp_dir, ['txt'], startlevel=1, endlevel=1) == file_path2

#     # Test 4: Get newest file with multiple extensions
#     with tempfile.TemporaryDirectory() as temp_dir:
#         file_path1 = os.path.join(temp_dir, 'test1.txt')
#         with open(file_path1, 'w') as f:
#             f.write('test1')
#         time.sleep(2)
#         file_path2 = os.path.join(temp_dir, 'test2.md')
#         with open(file_path2, 'w') as f:
#             f.write('test2')
#         assert mf.getNewestFile(temp_dir, ['txt', 'md']) == file_path2

#     # Test 5: Get newest file with no matching files
#     with tempfile.TemporaryDirectory() as temp_dir:
#         assert mf.getNewestFile(temp_dir, ['txt']) == ''

#     # Test 6: Get newest file with no existing directory
#     assert mf.getNewestFile('nonexistent_directory', ['txt']) == ''


def test_getFilesFromDirectory():
    with tempfile.TemporaryDirectory() as tmpdir:
        test_directory = tmpdir

        # Create some temporary files with different extensions
        with tempfile.NamedTemporaryFile(suffix=".txt", dir=tmpdir, delete=False):
            pass
        with tempfile.NamedTemporaryFile(suffix=".doc", dir=tmpdir, delete=False):
            pass

        # Create a subdirectory with a temporary file
        sub_dir = os.path.join(tmpdir, "subdir")
        os.mkdir(sub_dir)
        with tempfile.NamedTemporaryFile(suffix=".txt", dir=sub_dir, delete=False):
            pass

        # Case 1: The directory doesn't exist.
        with pytest.raises(ValueError):
            mf.getFilesFromDirectory("nonexistent_directory")

        # Case 2: No extensions are specified.
        files = mf.getFilesFromDirectory(test_directory, recursive=True)
        assert len(files) == 3  # We created 3 files

        # Case 3: One extension is specified.
        files = mf.getFilesFromDirectory(test_directory, exts=["txt"], recursive=True)
        assert len(files) == 2  # We created 2 txt files

        # Case 4: Multiple extensions are specified.
        files = mf.getFilesFromDirectory(test_directory, exts=["txt", "doc"], recursive=True)
        assert len(files) == 3  # We created 2 txt files and 1 doc file

        # Case 5: Files are sought in a directory recursively.
        files = mf.getFilesFromDirectory(test_directory, recursive=True)
        assert len(files) == 3  # We created 2 txt files and 1 doc file in root and subdirectories

        # Case 6: Files are sought in a directory non-recursively.
        files = mf.getFilesFromDirectory(test_directory, recursive=False)
        assert len(files) == 2  # We created 2 files in root directory

def test_getVideosFromDirectory():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create some temporary files with different extensions
        video_file = tempfile.NamedTemporaryFile(suffix=".mp4", dir=tmpdir, delete=False)
        video_file.close()
        text_file = tempfile.NamedTemporaryFile(suffix=".txt", dir=tmpdir, delete=False)
        text_file.close()

        # Case 1: Nonexistent directory.
        with pytest.raises(ValueError):
            mf.getVideosFromDirectory("nonexistent_directory")

        # Case 2: Get videos from directory.
        videos = mf.getVideosFromDirectory(tmpdir)
        assert len(videos) == 1  # We created 1 video file

        # Case 3: Recursive is set to True, but there's no subdirectory.
        videos = mf.getVideosFromDirectory(tmpdir, recursive=True)
        assert len(videos) == 1  # We created 1 video file

def test_getImagesFromDirectory():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create some temporary files with different extensions
        image_file = tempfile.NamedTemporaryFile(suffix=".jpg", dir=tmpdir, delete=False)
        image_file.close()
        text_file = tempfile.NamedTemporaryFile(suffix=".txt", dir=tmpdir, delete=False)
        text_file.close()

        # Case 1: Nonexistent directory.
        with pytest.raises(ValueError):
            mf.getImagesFromDirectory("nonexistent_directory")

        # Case 2: Get images from directory.
        images = mf.getImagesFromDirectory(tmpdir)
        assert len(images) == 1  # We created 1 image file

        # Case 3: Recursive is set to True, but there's no subdirectory.
        images = mf.getImagesFromDirectory(tmpdir, recursive=True)
        assert len(images) == 1  # We created 1 image file