# Multi-Character Composer

多角色 PV 自动导演器。

> **核心原则**：多角色 PV 不是「多个角色各自出场」，而是**用关系做卖点**。
> 如果去掉关系表达后 PV 依然成立，那它只是几支单角色 PV 的拼接。

---

## 导演链

```
Cast 定义（cast-schema）
    ↓
Contrast 校验（任意两人至少 2 维强对比）—— 不通过则拒绝
    ↓
Screen Weight 分配（lead >= second x 1.5）
    ↓
Framing Strategy（solo 60% / together 40%）
    ↓
Cast Risk Gate（同框人数放大动作等级）
    ↓
Shot Planner
    ↓
Quality Check（稳定性上限按人数封顶）
```

---

## 15s 双人 PV 结构（duo）

最成熟的多角色形态。推荐作为默认。

```
0-2s     LEAD HOOK        主角单人建立，禁止一开场就同框
2-4s     SECOND HOOK      次角单人建立，机位必须与 Shot1 不同
4-7s     INDIVIDUAL       各自能力/魅力，仍为分镜
7-10s    RELATIONSHIP     首次同框，关系镜头（本段是卖点核心）
10-13s   INTERPLAY        交替快切制造互动感，非真同框
13-15s   DUO FREEZE       双人定格 + 标题
```

**为什么把同框放在 7s 之后**：观众需要先分别记住两个人，才能理解他们的关系。
开场同框会导致两人都记不住。

---

## 15s 三人 PV 结构（trio）

```
0-1.5s   LEAD HOOK
1.5-3s   SECOND HOOK
3-4.5s   SUPPORT HOOK
4.5-8s   ROTATION         三人轮换独占，每人约 1.2s
8-11s    TRIO FORMATION   三人同框列队（低动作等级）
11-13s   INTERPLAY
13-15s   TRIO FREEZE
```

三人已接近同框上限，`TRIO FORMATION` 必须使用 `action_level 1` 组件。

---

## 30s 剧情双人 PV

关系张力最适合的时长。

```
0-5s     世界 + 主角
5-10s    次角登场，关系埋线
10-16s   关系冲突 / 对峙
16-23s   各自高光（分镜）
23-28s   并肩 / 和解 / 决裂
28-30s   双人定格
```

---

## 关系类型与镜头映射

| 关系 | 构图 | 推荐镜头 | 禁止 |
|---|---|---|---|
| rival 对手 | 对峙 / 背对背 | `duo-standoff`、`back-to-back` | 亲密贴近 |
| ally 同伴 | 并肩 | `shoulder-to-shoulder`、`duo-formation` | 对峙压迫 |
| mentor_student 师徒 | 高低位差 | `duo-formation`（高低错位） | 平等并列 |
| siblings 血亲 | 呼应姿态 | `mirrored-pose` | 敌对构图 |
| duo_unit 组合 | 同步动作 | `duo-formation`、`mirrored-pose` | 主次悬殊过大 |
| opposing 阵营对立 | 分割构图 | `split-frame-duo`、`duo-standoff` | 同框亲密 |

---

## 强制规则

1. **Lead 必须在首个 Shot 出现**，且首个 Shot 为单人
2. **每个成员至少 1 个独占 Shot**，否则沦为背景
3. **同框 Shot 的有效动作等级** = 组件等级 + (同框人数 - 1)
4. **同框构图锚位固定**：一旦确定 A 在左 B 在右，全片不得互换
5. **同框 Shot 禁止两人手部同时进入前景**
6. **Negative prompt 必须显式禁止角色特征互换**

---

## 关系镜头是卖点，不是装饰

自检：删掉所有同框/关系镜头后，这支 PV 是否还有存在意义？
如果答案是「有」，说明关系没有被真正利用，应重新设计。
