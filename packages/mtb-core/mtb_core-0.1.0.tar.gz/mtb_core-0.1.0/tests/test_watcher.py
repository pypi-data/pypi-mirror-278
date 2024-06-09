# import time
# from unittest.mock import Mock
#
# import pytest
#
# from mtb.core.watcher import Watcher
#
#
# @pytest.fixture
# def setup_watcher(tmp_path):
#     callback = Mock()
#     file_extension = ".txt"
#     watcher = Watcher(tmp_path, callback, file_extension)
#     return watcher, callback, tmp_path, file_extension
#
#
# def test_watcher_starts_and_stops(setup_watcher):
#     watcher, _, _, _ = setup_watcher
#     watcher.start()
#     watcher.stop()
#     watcher.join()
#
#
# def test_watcher_triggers_callback_on_file_modified(setup_watcher):
#     watcher, callback, tmp_path, file_extension = setup_watcher
#
#     watcher.start()
#     time.sleep(0.1)  # Give some time for the observer to start
#
#     test_file = tmp_path / f"test{file_extension}"
#     test_file.write_text("Hello, world!")
#     time.sleep(0.5)  # Give some time for the observer to notice the change
#
#     callback.assert_called_once()
#
#     watcher.stop()
#     watcher.join()
#
#
# def test_watcher_does_not_trigger_for_other_extensions(setup_watcher):
#     watcher, callback, tmp_path, _ = setup_watcher
#
#     watcher.start()
#     time.sleep(0.1)  # Give some time for the observer to start
#
#     test_file = tmp_path / "test.log"
#     test_file.write_text("Should not trigger callback.")
#
#     time.sleep(0.5)  # Give some time for the observer to notice the change
#
#     callback.assert_not_called()
#
#     watcher.stop()
#     watcher.join()
#
#
# def test_watcher_start_stop_exception(setup_watcher, mocker):
#     watcher, _, _, _ = setup_watcher
#     mocker.patch.object(watcher.observer, "start", side_effect=Exception("Cannot start"))
#     mocker.patch.object(watcher.observer, "stop", side_effect=Exception("Cannot stop"))
#
#     with pytest.raises(Exception, match="Cannot start"):
#         watcher.start()
#
#     with pytest.raises(Exception, match="Cannot stop"):
#         watcher.stop()
