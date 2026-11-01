#!/bin/bash
# 下载 1.21.8 客户端 JAR 并解出渲染需要的 blockstates / models / textures
set -e
DIR=${1:-$(dirname "$0")/mc}
mkdir -p "$DIR" && cd "$DIR"
if [ ! -f client.jar ]; then
  V=$(curl -s https://piston-meta.mojang.com/mc/game/version_manifest_v2.json | jq -r '.versions[]|select(.id=="1.21.8").url')
  curl -s -o client.jar "$(curl -s "$V" | jq -r .downloads.client.url)"
fi
rm -rf assets
unzip -q client.jar "assets/minecraft/blockstates/*" "assets/minecraft/models/*" "assets/minecraft/textures/block/*" -d .
echo "assets ready: $DIR/assets/minecraft"
