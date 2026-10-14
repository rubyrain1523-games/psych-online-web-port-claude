package sys.io;
#if macro


enum FileSeek {
	SeekBegin;
	SeekCur;
	SeekEnd;
}

#else


enum FileSeek {
	SeekBegin;
	SeekCur;
	SeekEnd;
}

#end
