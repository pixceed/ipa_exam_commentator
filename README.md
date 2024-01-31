# IPAの過去問を解説する

## Docker 環境構築

### プロキシ無し

イメージ作成

``` bash
docker build -t ipa_exam_commentator_image:1.0 build
```

コンテナ作成

``` bash
docker run -it -v `pwd`:/home/ubuntu/workspace -p 8501:8501 --name ipa_exam_commentator_container ipa_exam_commentator_image:1.0 bash
```

### プロキシあり

イメージ作成

``` bash
 docker build --no-cache --force-rm=true \
    --build-arg http_proxy=[PROXY] \
    --build-arg https_proxy=[PROXY] \
    -t ipa_exam_commentator_image:3.0 \
    build
```

コンテナ作成

``` bash
docker run -it \
    -v `pwd`:/home/ubuntu/workspace \
    --env HTTP_PROXY=[PROXY] \
    --env HTTPS_PROXY=[PROXY] \
    -p 8502:8502 \
    --name ipa_exam_commentator_container ipa_exam_commentator_image:3.0 bash
```

