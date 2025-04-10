# Python Packages

- ✅ python packages.

## Packages

| modules                 | desc               | rank       |
|:------------------------|:-------------------|:-----------|
| [bpstd](packages/bpstd) | common libs        | ⭐⭐         |
| [better-px](packages/px)          | 第三方库增强扩展 | ⭐⭐⭐ |
| [better-std](packages/std]          | 标准库增强扩展 | ⭐ |

## Usage

- uv + git:

```ruby
# add better-px:
uv add better-px

# add better-std:
uv add better-std

# add bpstd:
uv add git+https://github.com/better-py/pkg.git@main#packages/bpstd=subdir

```

## Intro

### [packages/bpstd](packages/bpstd)

- ✅ 开箱即用的 django 开发工具包
- ✅ 已集成大量 django 开发常用的工具库

## Requirements

### [packages/better-px]

> python 3rd party extensions.

- ✅ 集成大量 python `第三方热门库`的 工具库

### [packages/bpstd]

> common libs for `django` development.

- ✅ python 3.9+
- ✅ django
- ✅ django-rest-framework
- ✅ redis
- ✅ mysql
- ✅ rabbitmq
- ✅ celery

## Development

> install:

- ✅ [go-task](https://taskfile.dev/): 命令行脚本工具
  - [Taskfile](Taskfile.yml): 配置脚本， 替代 Makefile
- ✅ python 3.12+

```ruby

# install go-task:
brew install go-task

```

## References

- python package template: [template-python](https://github.com/jacebrowning/template-python)
