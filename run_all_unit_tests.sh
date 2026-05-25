#PYTHONPATH=. python3 -m pytest .

## activate Python3 virtualenv:                                                                                                                                                                                                        
. /home/vk/src/memacs/venv/bin/activate 

cd memacs
PYTHONPATH=.. pytest --exitfirst

#end
