import logging
import os
import queue
import threading
import time

from inotify_simple import INotify, flags

logger = logging.getLogger("filesystem.watcher")

def file_watcher(root_path,
                 dir_gone=None,
                 dir_moved=None,
                 file_created=None,
                 file_deleted=None,
                 file_gone=None,
                 file_modified=None,
                 file_moved=None):
    """
    dir_done(dir_path)
    dir_moved(dir_path, old_path)
    file_created(file_path)
    file_deleted(file_path)
    file_gone(file_path)
    file_modified(file_path)
    file_moved(file_path, old_path)
    """

    inotify = INotify()
    event_queue = queue.Queue()

    watch_flags = flags.CREATE | \
                  flags.MODIFY | \
                  flags.MOVED_TO | flags.MOVED_FROM  | \
                  flags.DELETE

    watch_paths = dict()
    moved_paths = dict()

    def add_watch(dir_path):
        wd = inotify.add_watch(dir_path, watch_flags)
        watch_paths[wd] = dir_path

    def walk_directory(dir_path):
        for root_path, dir_names, file_names in os.walk(dir_path):
            for file_name in file_names:
                file_path = os.path.join(root_path, file_name)
                event_queue.put({"name": "file_created", "file_path": file_path})
            for dir_name in dir_names:
                dir_path = os.path.join(root_path, dir_name)
                add_watch(dir_path)

    def watch_directory(dir_path):
        add_watch(dir_path)
        walk_directory(dir_path)

    def get_watch_descriptor(dir_path):
        wds = [wd for wd, path in watch_paths.items() if path == dir_path]
        return next(iter(wds), None)

    def get_moved_path(cookie):
        old_path = moved_paths.get(cookie, None)
        moved_paths.pop(cookie, None)
        return old_path

    def add_moved_path(cookie, path, isdir=None):
        moved_paths[cookie] = path

        def track_cookie(cookie, isdir):
            time.sleep(1)

            path = get_moved_path(cookie)
            if path is not None:
                if isdir is True:
                    event_queue.put({"name": "dir_gone", "dir_path": path})
                else:
                    event_queue.put({"name": "file_gone", "file_path": path})
                wd = get_watch_descriptor(path)
                if wd is not None:
                    del watch_paths[wd]
                    inotify.rm_watch(wd)

        thread = threading.Thread(target=track_cookie, daemon=True, kwargs={
            "cookie": cookie,
            "isdir": isdir,
        })

        thread.start()

    def watching_thread(root_path):
        watch_directory(root_path)

        while True:
            try:
                for event in inotify.read():
                    if event.mask & flags.IGNORED:
                        continue

                    dir_path = watch_paths[event.wd]
                    name_path = os.path.join(dir_path, event.name)

                    if event.mask & flags.ISDIR:
                        if event.mask & flags.CREATE:
                            watch_directory(name_path)
                        elif event.mask & flags.DELETE:
                            wd = get_watch_descriptor(name_path)
                            if wd is not None:
                                del watch_paths[wd]
                        elif event.mask & flags.MOVED_FROM:
                            add_moved_path(event.cookie, name_path, isdir=True)
                        elif event.mask & flags.MOVED_TO:
                            old_path = get_moved_path(event.cookie)
                            if old_path is not None:
                                event_queue.put({"name": "dir_moved", "dir_path": name_path, "old_path": old_path})
                                wd = get_watch_descriptor(old_path)
                                if wd is not None:
                                    watch_paths[wd] = name_path
                            else:
                                watch_directory(name_path)

                    else:
                        if event.mask & flags.CREATE:
                            event_queue.put({"name": "file_created", "file_path": name_path})
                        elif event.mask & flags.DELETE:
                            event_queue.put({"name": "file_deleted", "file_path": name_path})
                        elif event.mask & flags.MODIFY:
                            event_queue.put({"name": "file_modified", "file_path": name_path})
                        elif event.mask & flags.MOVED_FROM:
                            add_moved_path(event.cookie, name_path)
                        elif event.mask & flags.MOVED_TO:
                            old_path = get_moved_path(event.cookie)
                            if old_path is not None:
                                event_queue.put({"name": "file_moved", "file_path": name_path, "old_path": old_path})
                            else:
                                event_queue.put({"name": "file_created", "file_path": name_path})

            except KeyboardInterrupt:
                event_queue.join()
                break
            except Exception as err:
                logger.error(err, exc_info=True)

    def processing_thread(dir_moved=None,
                          dir_gone=None,
                          file_created=None,
                          file_deleted=None,
                          file_gone=None,
                          file_modified=None,
                          file_moved=None):
        while True:
            try:
                event = event_queue.get()

                name = event["name"]
                del event["name"]

                if name == "dir_moved" and dir_moved is not None:
                    dir_moved(**event)
                elif name == "dir_gone" and dir_gone is not None:
                    dir_gone(**event)
                elif name == "file_created" and file_created is not None:
                    file_created(**event)
                elif name == "file_deleted" and file_deleted is not None:
                    file_deleted(**event)
                elif name == "file_gone" and file_gone is not None:
                    file_gone(**event)
                elif name == "file_modified" and file_modified is not None:
                    file_modified(**event)
                elif name == "file_moved" and file_moved is not None:
                    file_moved(**event)

                event_queue.task_done()

            except KeyboardInterrupt:
                break
            except Exception as err:
                logger.error(err, exc_info=True)

    threads = list()

    threads.append(threading.Thread(target=watching_thread, daemon=True, kwargs={
        "root_path": root_path,
    }))

    threads.append(threading.Thread(target=processing_thread, daemon=True, kwargs={
        "dir_moved": dir_moved,
        "dir_gone": dir_gone,
        "file_created": file_created,
        "file_deleted": file_deleted,
        "file_gone": file_gone,
        "file_modified": file_modified,
        "file_moved": file_moved,
    }))

    for thread in threads:
        thread.start()
