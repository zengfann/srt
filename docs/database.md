# 数据库设计

## user 表

```json
{
    "id": 1,
    "username": "jack",
    "password": "jack1234"
}
```

## dataset 表

### 权限
| 角色    | 权限                                                            |
| :------ | :-------------------------------------------------------------- |
| creator | add checked sample, delete sample, check sample, delete dataset |
| manager | add checked sample, delete sample, check sample                 |
| others  | add unchecked sample                                            |

```json
{
    "id": 1,
    "name": "西瓜",
    "creator": "jack",
    "labels": {
        "瓜柄": {
            "type": "num",
            "max": 100,
            "min": 0,
            "description": "瓜柄的长度(cm)" 
        },
        "颜色": {
            "type": "enum",
            "values": ["绿色", "红色"],
            "description": "瓜的颜色" 
        }
    },
    "managers": ["jack", "rose"]
}

{
    "id": 2,
    "name": "橘子",
    "creator": "rose",
    "labels": {
        "直径": {
            "type": "num",
            "max": 30,
            "min": 0,
            "description": "橘子的直径(cm)" 
        }
    },
    "managers": ["jack", "rose"]
}
```

## sample 表

```json
{
    "id": 1,
    "dataset": 1,
    "labels": {
        "瓜柄": 12,
        "颜色": "绿色"
    },
    "checked": true
}

{
    "id": 2,
    "dataset": 1,
    "label": {
        "瓜柄": 7,
        "颜色": "红色"
    },
    "checked": false
}

{
    "id": 3,
    "dataset": 2,
    "labels": {
        "直径": 5
    },
    "checked": true
}

{
    "id": 4,
    "dataset": 2,
    "labels": {
        "直径": 6
    },
    "checked": true
}
```

> dataset --- 1:n --> sample
