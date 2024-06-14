import os
import sys

class dump_output:
    '''
    Class used to grab standard output or another stream, taken from:
    https://stackoverflow.com/questions/24277488/in-python-how-to-capture-the-stdout-from-a-c-shared-library-to-a-variable
    '''
    escape_char = '\b'
    #-----------------------------------------------------
    def __init__(self):
        self.origstream   = sys.stdout
        self.origstreamfd = self.origstream.fileno()
        self._text        = '' 
        self._stopped     = None 

        # Create a pipe so the stream can be captured:
        self.pipe_out, self.pipe_in = os.pipe()

        self._start()
    #-----------------------------------------------------
    def _start(self):
        '''
        Start capturing the stream data.
        '''
        # Save a copy of the stream:
        self.streamfd = os.dup(self.origstreamfd)

        # Replace the original stream with our write pipe:
        os.dup2(self.pipe_in, self.origstreamfd)

        self._stopped = False
    #-----------------------------------------------------
    def _read_output(self):
        '''
        Read the stream data (one byte at a time)
        and save the text in `capturedtext`.
        '''
        while True:
            char = os.read(self.pipe_out, 1)
            if not char or bytes(self.escape_char, 'utf-8') in char:
                break

            self._text += char.decode('utf-8')
    #-----------------------------------------------------
    def _stop(self):
        '''
        Stop capturing the stream data and save the text in `capturedtext`.
        '''
        if self._stopped:
            return

        # Print the escape character to make the readOutput method stop:
        self.origstream.write(self.escape_char)

        # Flush the stream to make sure all our data goes in before
        # the escape character:
        self.origstream.flush()
        self._read_output()

        # Close the pipe:
        os.close(self.pipe_in)
        os.close(self.pipe_out)

        # Restore the original stream:
        os.dup2(self.streamfd, self.origstreamfd)

        # Close the duplicate stream:
        os.close(self.streamfd)

        self._stopped = True
    #-----------------------------------------------------
    def retrieve(self):
        self._stop()

        return self._text
#-------------------------

