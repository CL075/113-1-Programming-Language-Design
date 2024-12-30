# 113-1 Programming Language Design Fianl Project
## Group 26
113522057 蔡佩蓉
<br>
113522116 翁沁翎

## 簡易開關
若要關閉功能5~7，可將底下的```feature_5```、```feature_6```、```feature_7```改為```False```。
```
FEATURE_FLAGS = {
    "feature_1": True,
    "feature_2": True,
    "feature_3": True,
    "feature_4": True,
    "feature_5": True,
    "feature_6": True,
    "feature_7": True,
}
```

## 範例輸入輸出

創建使用者
```
1. Create a user

Enter username: user1

Create a user named "user1".
```

創建sheet (可自行設定要多大的矩陣)
```
2. Create a sheet

Enter username and sheet name: user1 sheet
Enter number of rows and columns: 3 3

Create a sheet named "sheet" with size 3x3 for "user1".
```

確認sheet的值
```
3. Check a sheet

Enter username and sheet name: user1 sheet

Sheet content:
0, 0, 0
0, 0, 0
0, 0, 0
```

更改sheet裡面的值
```
4. Change a value in a sheet

Enter username and sheet name: user1 sheet
Sheet content (owner: user1):
0, 0, 0
0, 0, 0
0, 0, 0

Enter row, col, and expression: 1 2 3
Value updated.
0, 0, 0
0, 0, 3
0, 0, 0
```

更改使用者對於sheet的權限 (這裡的使用者指的是創建sheet的那個人)
```
5. Change a sheet's access right.

Enter username, sheet name, and access right: user1 sheet ReadOnly

Access rights for sheet updated.
```

共享sheet給另一個使用者 (在輸入的時候就可以設定是要分享怎樣的權限給另一個人)
```
6. Collaborate with another user

Enter owner, sheet name, collaborator, and access right: user1 sheet user2 Editable

Access right updated for user2.
```

更改被分享人的權限 (被分享人->指創建sheet以外的人)
```
7. Modify shared user's access right

Enter owner, sheet name, collaborator, and new access right: user1 sheet user2 ReadOnly

Updated "user2"'s access to "ReadOnly" for "sheet".
```
