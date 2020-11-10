import selectors
import subprocess
import sys
import os

def run_subprocess(cmd_list, log_file_object=None, return_error=True, return_output=False, log_output=True,
                    log_command=True):
    if log_command:
        if log_file_object:
            print(f"executing subprocess {cmd_list}", file=log_file_object)
        else:
            print(f"executing subprocess {cmd_list}")

    drain_output = False
    if return_output:
        stdout = subprocess.PIPE
        drain_output = True
    elif log_output:
        if log_file_object:
            stdout = log_file_object
        else:
            stdout = subprocess.PIPE
            drain_output = True
    else:
        stdout = None

    drain_error = False
    if return_error:
        stderr = subprocess.PIPE
        drain_error = True
    elif log_output:
        stderr = subprocess.STDOUT
    else:
        stderr = None

    process = subprocess.Popen(cmd_list, stdout=stdout, stderr=stderr)

    output_bytes = bytearray() if return_output else None
    error_bytes = bytearray() if return_error else None
    if drain_output or drain_error:
        with selectors.DefaultSelector() as sel:
            if drain_output:
                sel.register(process.stdout, selectors.EVENT_READ)
            if drain_error:
                sel.register(process.stderr, selectors.EVENT_READ)
            while drain_output or drain_error:
                for key, _ in sel.select():
                    data_bytes = key.fileobj.read1(4096)
                    if not data_bytes:
                        if key.fileobj is process.stdout:
                            drain_output = False
                        elif key.fileobj is process.stderr:
                            drain_error = False
                    if key.fileobj is process.stdout:
                        if return_output:
                            output_bytes += data_bytes
                        if log_output:
                            if log_file_object:
                                os.write(log_file_object.fileno(), data_bytes)
                                log_file_object.flush()
                            else:
                                os.write(sys.stdout.fileno(), data_bytes)
                                sys.stdout.flush()
                    if key.fileobj is process.stderr:
                        if return_error:
                            error_bytes += data_bytes
                        if log_output:
                            if log_file_object:
                                os.write(log_file_object.fileno(), data_bytes)
                                log_file_object.flush()
                            else:
                                os.write(sys.stderr.fileno(), data_bytes)
                                sys.stderr.flush()
    rc = process.poll()
    return rc, output_bytes.decode() if output_bytes else None, error_bytes.decode() if error_bytes else None

with open("xxx", "w") as fd:
    rc, out, err = run_subprocess(['/bin/bash', '-c', './t.sh'], return_output=False, log_file_object=None)
    print(f"rc: {rc}")
    print(f"out: [{out}]")
    print(f"err: [{err}]")
