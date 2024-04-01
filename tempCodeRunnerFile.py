hread = threading.Thread(target=continuousLoop)
thread.daemon = True
thread.start()