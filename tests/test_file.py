import pytest
import os
import tempfile
import zipfile

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

def test_getFilesFromDirectory():
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a file in the temporary directory
        file_path = os.path.join(temp_dir, 'test.txt')
        with open(file_path, 'w') as f:
            f.write('test')

        # Test getFilesFromDirectory
        files = mf.getFilesFromDirectory(temp_dir, exts=['txt'])
        assert files == [file_path]

def test_getVideosFromDirectory():
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a video file in the temporary directory
        video_path = os.path.join(temp_dir, 'test.mp4')
        with open(video_path, 'w') as f:
            f.write('test')

        # Test getVideosFromDirectory
        videos = mf.getVideosFromDirectory(temp_dir)
        assert videos == [video_path]

def test_getImagesFromDirectory():
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create an image file in the temporary directory
        image_path = os.path.join(temp_dir, 'test.jpg')
        with open(image_path, 'w') as f:
            f.write('test')

        # Test getImagesFromDirectory
        images = mf.getImagesFromDirectory(temp_dir)
        assert images == [image_path]

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

def test_removeFile():
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a file in the temporary directory
        file_path = os.path.join(temp_dir, 'test.txt')
        with open(file_path, 'w') as f:
            f.write('test')

        # Test removeFile
        assert mf.removeFile(file_path)

        # Check if the file was removed
        assert not os.path.isfile(file_path)

        # Test removeFile with a non-existent file
        assert mf.removeFile(file_path)

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
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, 'test.txt')

        # Create file
        with open(file_path, 'w') as f:
            f.write('test')

        # Test delete
        mf.delete(file_path)

        # Check if the file is deleted
        assert not os.path.isfile(file_path)

        # Test delete with a non-existent file
        assert not mf.delete(file_path)

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