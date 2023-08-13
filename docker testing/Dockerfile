FROM public.ecr.aws/sam/build-python3.9

WORKDIR /code
COPY /entrypoint.sh /script/entrypoint.sh

CMD ["sh", "/script/entrypoint.sh"]
# ENTRYPOINT "/bin/bash"