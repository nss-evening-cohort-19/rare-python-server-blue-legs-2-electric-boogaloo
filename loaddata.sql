CREATE TABLE "Users" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "first_name" varchar,
  "last_name" varchar,
  "email" varchar,
  "bio" varchar,
  "username" varchar,
  "password" varchar,
  "profile_image_url" varchar,
  "created_on" date,
  "active" bit
);

CREATE TABLE "DemotionQueue" (
  "action" varchar,
  "admin_id" INTEGER,
  "approver_one_id" INTEGER,
  FOREIGN KEY(`admin_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`approver_one_id`) REFERENCES `Users`(`id`),
  PRIMARY KEY (action, admin_id, approver_one_id)
);


CREATE TABLE "Subscriptions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "follower_id" INTEGER,
  "author_id" INTEGER,
  "created_on" date,
  FOREIGN KEY(`follower_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Posts" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "category_id" INTEGER,
  "title" varchar,
  "publication_date" date,
  "image_url" varchar,
  "content" varchar,
  "approved" bit,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Comments" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "author_id" INTEGER,
  "content" varchar,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Reactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar,
  "image_url" varchar
);

CREATE TABLE "PostReactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "reaction_id" INTEGER,
  "post_id" INTEGER,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`reaction_id`) REFERENCES `Reactions`(`id`),
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`)
);

CREATE TABLE "Tags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);

CREATE TABLE "PostTags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "tag_id" INTEGER,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`tag_id`) REFERENCES `Tags`(`id`)
);

CREATE TABLE "Categories" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);


INSERT INTO Categories ('label') VALUES ('News');
INSERT INTO Tags ('label') VALUES ('JavaScript');
INSERT INTO PostTags ('post_id', 'tag_id') VALUES (7, 7);
INSERT INTO Reactions ('label', 'image_url') VALUES ('happy', 'https://pngtree.com/so/happy');


INSERT INTO Subscriptions VALUES (null, 1, 1, "10/31/2022");
INSERT INTO Posts VALUES (null, 1, 3, "Test Title 2", "10/33/2022", "https://res.cloudinary.com/twofiveclimb/image/upload/v1666979419/mad-app/e5sgpxaykaxqsls5kavg.jpg", "This is the second test.  Test Test Scary", True);
INSERT INTO Comments VALUES (null, 2, 1, "This is also delightful");
INSERT INTO Reactions VALUES (null, "Mad", 'https://pngtree.com/so/mad');
INSERT INTO PostReactions VALUES (null, 1, 1, 1);
INSERT INTO Tags VALUES (null, "Python");
INSERT INTO PostTags VALUES (null, 4, 1);
INSERT INTO Categories VALUES (null, 'Coding');
INSERT INTO PostReactions VALUES (null, 1, 2, 2);
INSERT INTO Reactions VALUES (null, "Sad", 'https://pngtree.com/so/mad');
INSERT INTO PostReactions VALUES (null, 1, 3, 1);

SELECT
    r.id,
    r.label,
    r.image_url,
    pr.id post_reaction_id,
    pr.reaction_id reaction_id
FROM reactions r
JOIN postreactions pr
    ON r.id = pr.reaction_id

DELETE
FROM reactions r
JOIN postreactions pr
  ON r.id = pr.reaction_id
WHERE r.id = 6

-- SELECT                  
--             c.id,
--             c.author_id,
--             c.post_id,
--             c.content,
--             u.first_name,
--             u.last_name
--         FROM comments c
--         JOIN users u
--             ON c.author_id = u.id

SELECT
      c.id,
      c.id,
      c.author_id,
      c.post_id,
      c.content
FROM comments c
JOIN posts p
ON p.id = c.post_id
WHERE c.post_id = 1
        
