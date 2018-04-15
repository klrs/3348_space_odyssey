import mysql.connector
import random

db = mysql.connector.connect(host="localhost",
                             user="dbuser6",
                             passwd="dbpass6",
                             db="odyssey3348",
                             buffered=True)


def show_location(loc):
    cur = db.cursor()
    sql = "SELECT LocDescription, LocationName FROM location WHERE LocationId='" + loc + "'"
    cur.execute(sql)
    for row in cur:
        print(70 * '-')
        print(row[1])
        print(70 * '-')
        myprint(row[0])

    return


def show_passages(loc):
    print("\nThe possible exits are:"),
    cur = db.cursor()
    sql = "SELECT LocationName, LockPrompt FROM PASSAGE INNER JOIN location ON PASSAGE.arrivalloc = location.locationid  WHERE departureloc=" + loc
    cur.execute(sql)
    i = 0;
    for row in cur.fetchall():
        print(row[0], end=' ')
        i = i + 1
        if row[1] != '':
            print("(" + row[1] + ")", end=' ')
        if i < cur.rowcount:
            print("")
    print("")
    return


def move(loc, target, comp):
    result = loc
    cur = db.cursor()
    sql = "SELECT ArrivalLoc FROM passage INNER JOIN location ON passage.ArrivalLoc = location.LocationId WHERE Locked = 0 AND DepartureLoc ='" + loc + "' AND LocationName LIKE '%" + target + "%'"
    cur.execute(sql)
    if cur.rowcount == 1:
        for row in cur.fetchall():
            result = str(row[0])
            cur = db.cursor()
            sql = "UPDATE PLAYERCHARACTER SET PLAYERCHARACTER.LocationId = '" + result + "' WHERE PLAYERCHARACTER.PLAYERNAME = '" + str(
                "Pan Bannister") + "' OR PLAYERCHARACTER.PLAYERID = '" + str(comp) + "';"
            cur.execute(sql)
            story(result, comp)
            if get_enemy_count_in_loc(result) >= 1:
                done = combat(result, comp)
                if done == str("GAME OVER"):
                    result = done
            if result != 'GAME OVER':
                story(result, comp)
                show_location(result)
                enemy_scan(result)
                showDropped(result);
                show_passages(result)
    elif cur.rowcount > 1:
        print("I can only go to one place at a time! Please be more specific.");
    else:
        print("You can't go there.");
    return result


###########   INVENTORY AND GEAR MANAGEMENT  ###################################

def deleteDupes(items):
    # dumbass function to determine if there's two same results (like unarmed) in items.
    # deletes duplicates from items and returns the new items list
    if len(items) > 1:
        i = len(items);
        while 1 < i:
            if items[0][0] == items[i - 1][0]:
                del items[i - 1]
            i = i - 1;
        print(len(items));

    return items;


def showInv(comp):
    cur = db.cursor();

    sql = "SELECT itemtype.ItemTypeName, item.playerid, item.itemid FROM item INNER JOIN itemtype ON itemtype.ItemTypeId = item.ItemTypeId WHERE item.PlayerId = 1 OR item.playerid = " + comp + ";";
    characters = ["Pan Bannister", "Chifundo", "Leesa"];
    cur.execute(sql);
    items = cur.fetchall();
    print("Items in your inventory:")
    for i in items:
        sql2 = "SELECT DISTINCT playercharacter.PlayerName FROM playercharacter INNER JOIN item ON Armor = " + str(
            i[2]) + " OR Weapon = " + str(i[2]) + ";"
        cur.execute(sql2);
        characters = cur.fetchall();

        if i[1] > 0:
            # if character is equipping the item
            if len(characters) != 0:
                print(i[0] + "(Equipped by " + characters[0][0] + ")");
            # if nobody is equipping item
            else:
                print(i[0]);
        # if item is not equippable
        else:
            print(i[0]);
    # print stats
    print_playerstats(comp, False)
    return


def showDropped(loc):
    cur = db.cursor();
    sql = "SELECT itemtype.ItemTypeName FROM itemtype INNER JOIN item ON item.ItemTypeId = itemtype.ItemTypeId WHERE item.LocationId = " + loc + ";";
    cur.execute(sql);
    items = cur.fetchall();

    for i in items:
        print("You see a " + i[0] + ".");


def pickItem(loc, targ):
    cur = db.cursor();
    sql = "SELECT itemtype.ItemTypeName, item.itemid FROM item INNER JOIN itemtype ON item.ItemTypeId = itemtype.ItemTypeId WHERE itemtype.ItemTypeName LIKE '%" + targ + "%' AND item.LocationId = " + loc + ";";
    cur.execute(sql);
    i = cur.fetchall();
    items = deleteDupes(i);

    if not items:
        print("There is no such item!");
    elif len(items) == 1:
        sql2 = "UPDATE item SET item.LocationId = NULL, item.PlayerId = 1 WHERE item.ItemId = " + str(
            items[0][1]) + ";";
        cur.execute(sql2);
        print("Picked up " + str(items[0][0]) + "!");
    else:
        print("Please be more specific!");


def checkComp(comp, value):
    possible = False;
    if value == comp or value == "1":
        possible = True;

    return possible;


def checkItemType(isArm, isWep):
    # checks item type and returns number
    # 0 for not equippable, 1 for weapon, 2 for armor
    itemtype = 0;

    if isArm == 1:
        itemtype = 2;
    elif isWep == 1:
        itemtype = 1;

    return itemtype;


def equipItem(targ, comp):
    ### NEEDS TESTING ###
    ### PROBABLY GIVES ACCESS TO COMPANIONS STUFF PLAYER DIDN'T CHOOSE!!! ###
    cur = db.cursor();
    sql = "SELECT DISTINCTROW itemtype.ItemTypeName, item.itemid, itemtype.IsArmor, itemtype.IsWeapon FROM itemtype INNER JOIN item ON item.itemtypeid = itemtype.itemtypeid WHERE itemtype.ItemTypeName LIKE '%" + targ + "%' AND item.PlayerId > 0;";
    cur.execute(sql);
    i = cur.fetchall();
    items = deleteDupes(i);

    if not items:
        print("There is no such item");
    elif len(items) == 1:
        print("Who do you want to equip it for? Select by typing number.");
        if comp == '2':
            equipfor = input("1. Pan Bannister\n2. Chifundo\n");
        elif comp == '3':
            equipfor = input("1. Pan Bannister\n3. Leesa\n");
        else:
            equipfor = input("1. Pan Bannister\n");

        if checkComp(comp, equipfor):
            # checks whether item is already equipped
            sql2 = "SELECT PlayerName, playerid FROM playercharacter WHERE weapon = " + str(
                items[0][1]) + " OR armor = " + str(items[0][1]) + ";";
            # update item.playerid
            sqlitem = "";
            # update playercharacter armor & weapon
            sqlpc = "";
            itemtype = checkItemType(items[0][2], items[0][3]);
            cur.execute(sql2);
            pitems = cur.fetchall();
            if not pitems:  # if nobody is equipping said item
                sqlitem = "UPDATE item SET playerid = " + equipfor + " WHERE itemid = " + str(items[0][1]) + ";";

                if itemtype == 1:
                    sqlpc = "UPDATE playercharacter SET weapon = " + str(
                        items[0][1]) + " WHERE playerid = " + equipfor + ";";
                elif itemtype == 2:
                    sqlpc = "UPDATE playercharacter SET armor = " + str(
                        items[0][1]) + " WHERE playerid = " + equipfor + ";";
                else:
                    print("Item not equipable!");
            else:  # if the item is already equipped by someone
                sqlitem = "UPDATE item SET playerid = " + equipfor + " WHERE itemid = " + str(items[0][1]) + ";";
                sqldel = "";

                if itemtype == 1:
                    sqldel = "UPDATE playercharacter SET weapon = NULL WHERE playerid != " + equipfor + " AND weapon = " + str(
                        items[0][1]) + ";";
                    sqlpc = "UPDATE playercharacter SET weapon = " + str(
                        items[0][1]) + " WHERE playerid = " + equipfor + ";";
                elif itemtype == 2:
                    sqldel = "UPDATE playercharacter SET armor = NULL WHERE playerid != " + equipfor + " AND armor = " + str(
                        items[0][1]) + ";";
                    sqlpc = "UPDATE playercharacter SET armor = " + str(
                        items[0][1]) + " WHERE playerid = " + equipfor + ";";
                else:
                    print("Item not equipable!");

                cur.execute(sqldel);

            cur.execute(sqlitem);
            cur.execute(sqlpc);
            print("Item equipped!");
        else:
            print("Invalid command!");
    else:
        print("Please be more specific!");


def examine(loc, targ, comp):
    cur = db.cursor();
    sql = "SELECT itemtypedescription, isarmor, isweapon, mindmg, maxdmg, dmgreduction FROM itemtype INNER JOIN item ON item.itemtypeid = itemtype.itemtypeid WHERE (playerid = 1 OR playerid = " + comp + " OR locationid = " + loc + ") AND itemtype.itemtypename LIKE '%" + targ + "%';";
    cur.execute(sql);
    i = cur.fetchall();
    items = deleteDupes(i);

    if not items:
        print("No such item!");
    elif len(items) == 1:
        itemtype = checkItemType(items[0][1], items[0][2]);

        myprint(items[0][0]);
        if itemtype == 1:
            print("Min dmg: " + str(items[0][3]) + " - Max dmg: " + str(items[0][4]));
        elif itemtype == 2:
            print("Dmg reduction: " + str(items[0][5]));
    # ADD YOUR OWN EXCEPTIONS!
    # elif target == "escape pod":
    #   koodia
    else:
        print("Please be more specific!");


###################################################################################

def hacking(loc, target):
    result = 0
    cur = db.cursor();
    sql = "SELECT LockCode FROM passage INNER JOIN location ON passage.ArrivalLoc = location.LocationId WHERE HackableLock = 1 AND DepartureLoc ='" + loc + "' AND LocationName LIKE '%" + target + "%'"
    cur.execute(sql);
    # for row in cur.fetchall():
        # print(row, " tässä")
    if cur.rowcount == 1:
        print('\nYou can quit hacking by inputting "q".')
        while result == 0:
            sql = "SELECT LockCode FROM passage INNER JOIN location ON passage.ArrivalLoc = location.LocationId WHERE HackableLock = 1 AND DepartureLoc ='" + loc + "' AND LocationName LIKE '%" + target + "%'"
            cur.execute(sql);
            for row in cur.fetchall():
                # print(row)
                l = []
                n = str(row[0])
                x = len(n)
                for i in range(0, x):
                    l.append(n[i])
                # print(l)
            k = []
            correctp = int(0)
            correctn = int(0)
            print('\nInput a', len(l), 'digit code from 0-9 open door.\n')
            for i in range(1, len(l) + 1):
                num = (input('Give ' + str(i) + '. number of the code: '))
                if num == 'q':
                    show_location(loc)
                    show_passages(loc)
                    showDropped(loc);
                    return
                k.append(num)
            print('\nThe code you inputted:', end='\r')
            print(*k, sep='-')
            # print(k)
            if l == k:
                result = 1
                cur = db.cursor();
                sql = "UPDATE passage INNER JOIN location ON passage.ArrivalLoc = location.LocationId SET HackableLock = 0, Locked = 0, LockPrompt ='This door is open.' WHERE HackableLock = 1 AND DepartureLoc ='" + loc + "' AND LocationName LIKE '%" + target + "%'"
                cur.execute(sql);
                cur = db.cursor();
                sql = "SELECT LockCode FROM passage INNER JOIN location ON passage.ArrivalLoc = location.LocationId WHERE HackableLock = 1 AND DepartureLoc ='" + loc + "' AND LocationName LIKE '%" + target + "%'"
                cur.execute(sql);
                print('\nThe code you gave is correct. The door is now open.\n')
                show_location(loc)
                show_passages(loc)
                showDropped(loc);
            else:
                for i in range(0, len(l)):
                    if k[i] == l[i]:
                        correctp = correctp + 1
                for i in k:
                    if i in l:
                        correctn = correctn + 1
                        l.remove(i)
                # print(l)
                # print(row)
                myprint('\nThere was ' + str(correctn) + ' digit(s) right in your code and ' + str(correctp) +
                      ' digit(s) in the right position. The door remains locked.')
    elif cur.rowcount > 1:
        print("Be more specific.")
    else:
        print("This door cannot be hacked!")

    return


def story(loc, comp):
    cur = db.cursor();
    sql = "SELECT StoryId, Textblock, VariationId FROM storycontainer WHERE Used = 0 AND LocationId = '" + loc + "'"
    cur.execute(sql);
    for row in cur.fetchall():
        if str(row[2]) == comp:
            c = str(row[0])
            f = row[2]
            myprint(row[1])
            input("\nPress enter to continue...")
            cur = db.cursor();
            sql = "UPDATE storycontainer SET Used = 1 WHERE VariationId =" + comp + " AND StoryId =" + c + " AND Used = 0 AND LocationId = '" + loc + "'"
            cur.execute(sql);
            cur = db.cursor();
            sql = "SELECT StoryId, Textblock, VariationId FROM storycontainer WHERE Used = 0 AND LocationId = '" + loc + "'"
            cur.execute(sql);
            print("")
        elif str(row[2]) == str(1):
            c = str(row[0])
            f = row[2]
            myprint(row[1])
            input("\nPress enter to continue...")
            cur = db.cursor();
            sql = "UPDATE storycontainer SET Used = 1 WHERE VariationId = 1 AND StoryId ='" + c + "' AND Used = 0 AND LocationId = '" + loc + "'"
            cur.execute(sql);
            cur = db.cursor();
            sql = "SELECT StoryId, Textblock, VariationId FROM storycontainer WHERE Used = 0 AND LocationId = '" + loc + "'"
            cur.execute(sql);
            print("")
    return


# ------------------use_start------------------

def use_jailcellkeycard(loc, target):
    comp = '0'
    cur = db.cursor();
    sql = "SELECT itemid FROM item WHERE PlayerId = 1 AND itemid = 1"
    cur.execute(sql);
    if cur.rowcount >= 1:
        # select leesa or chifundo
        l = 1
        while l == 1:
            choice = input("\nWhich cell do you want to open? (1 for woman cell, 2 for man cell): ")
            print('')
            if choice == '1':
                comp = '3'
                cur = db.cursor();
                sql = "UPDATE passage SET Locked = 0, LockPrompt = 'The elevator door is now open.' WHERE PassageId = '3-4'"
                cur.execute(sql);
                sql = "UPDATE passage SET Locked = 0, LockPrompt = 'This cell door is now open.' WHERE PassageId = '3-7' OR PassageId = '7-3'"
                cur.execute(sql);
                sql = "UPDATE enemy SET LocationId = 220 WHERE EnemyId = 31"
                cur.execute(sql);
                sql = "UPDATE item SET PlayerId = NULL WHERE PlayerId = 2"
                cur.execute(sql);
                sql = "UPDATE item SET PlayerId = NULL WHERE ItemId = 1"
                cur.execute(sql);
                l = 0
            elif choice == '2':
                comp = '2'
                sql = "UPDATE passage SET Locked = 0, LockPrompt = 'The elevator door is now open.' WHERE PassageId = '3-4'"
                cur.execute(sql);
                sql = "UPDATE passage SET Locked = 0, LockPrompt = 'This cell door is now open.' WHERE PassageId = '3-6' OR PassageId = '6-3'"
                cur.execute(sql);
                sql = "UPDATE enemy SET LocationId = 220 WHERE EnemyId = 30"
                cur.execute(sql);
                sql = "UPDATE item SET PlayerId = NULL WHERE PlayerId = 3"
                cur.execute(sql);
                sql = "UPDATE item SET PlayerId = NULL WHERE ItemId = 1"
                cur.execute(sql);
                l = 0
            else:
                print("Invalid choice!")
        return comp

    else:
        print("You can't use that!")
        return comp


def use_icepod(loc, target, comp):
    cur = db.cursor();
    sql = "SELECT itemid FROM item WHERE PlayerId = 1 AND itemid = 2"
    cur.execute(sql);
    if cur.rowcount == 1:
        if comp == '2':
            sql = "UPDATE item SET PlayerId = 2 WHERE itemid = 43"
            cur.execute(sql);
            sql = "UPDATE playercharacter SET Weapon = 43 WHERE PlayerId = 2"
            cur.execute(sql);
        elif comp == '3':
            sql = "UPDATE item SET PlayerId = 3 WHERE itemid = 42"
            cur.execute(sql);
            sql = "UPDATE playercharacter SET Weapon = 42 WHERE PlayerId = 3"
            cur.execute(sql);

        sql = "UPDATE item SET PlayerId = 1 WHERE itemid = 44"
        cur.execute(sql);
        sql = "UPDATE playercharacter SET Weapon = 44 WHERE PlayerId = 1"
        cur.execute(sql)
        loc = '201'
    else:
        print(
            "You remember the CD in Jaw Storage and somehow it seems really important... maybe you should go take it. Just in case.")
    return loc


def use_elevatorkeycard(loc, target):
    cur = db.cursor();
    sql = "SELECT itemid FROM item WHERE PlayerId = 1 AND itemid = 40"
    cur.execute(sql);
    if cur.rowcount == 1:
        cur = db.cursor();
        sql = "UPDATE passage SET Locked = 0, LockPrompt = 'This door is now open.' WHERE PassageId = '13_17'"
        cur.execute(sql);
        sql = "UPDATE item SET PlayerId = NULL WHERE ItemId = 40"
        cur.execute(sql);
        sql = "UPDATE storycontainer SET Used = 0 WHERE StoryId = 19"
        cur.execute(sql);
        story(loc, comp)
        show_location(loc)
        show_passages(loc)
        showDropped(loc);
    else:
        print("You can't use that!")
    return


def use_egckeycard(loc, target):
    cur = db.cursor();
    sql = "SELECT itemid FROM item WHERE PlayerId = 1 AND itemid = 41"
    cur.execute(sql);
    if cur.rowcount == 1:
        cur = db.cursor();
        sql = "UPDATE passage SET Locked = 0, LockPrompt = 'This door is now open.' WHERE PassageId = '5_6'"
        cur.execute(sql);
        sql = "UPDATE storycontainer SET Used = 0 WHERE StoryId = 23"
        cur.execute(sql);
        story(loc, comp)
        show_location(loc)
        show_passages(loc)
        showDropped(loc);
    else:
        print("You can't use that!")
    return


def use_cd(loc, target, comp):
    d = 0
    cur = db.cursor();
    sql = "UPDATE storycontainer SET Used = 0 WHERE StoryId = 30"
    cur.execute(sql);
    story(loc, comp)
    while d == 0:
        choice = input("What do you do? (1 to press Accept, 2 to press Cancel): ")
        if choice == '1':
            loc = '301'
            story(loc, comp)
            done = 1
            d = 1
            print("Congratulations! You saved the galaxy! Thank you for playing!")
        elif choice == '2':
            loc = '302'
            story(loc, comp)
            done = 1
            d = 1
            print("You are dead. The galaxy is doomed!")
        else:
            print("Invalid option.")

    return done


def use_powersupply(loc, target, comp):
    cur = db.cursor();
    sql = "UPDATE storycontainer SET Used = 0 WHERE StoryId = 18"
    cur.execute(sql);
    sql = "UPDATE passage SET Locked = 0, LockPrompt = 'This door is now open.' WHERE PassageId = '9_11'"
    cur.execute(sql);
    story(loc, comp)
    return


def use_telecom(loc, target, comp):
    cur = db.cursor();
    sql = "UPDATE storycontainer SET Used = 0 WHERE StoryId = 22"
    cur.execute(sql);
    story(loc, comp)
    return


# ------------------use_end------------------


# Format enemies into starting conditions; Should be used only at the start of a new game
def format_enemies():
    cur = db.cursor();
    sql = "SELECT ITEMTYPE.ADDSTR, ENEMYTYPE.MAXHP, ENEMYTYPE.MAXSTR, ENEMYTYPE.ENEMYTYPEID, ENEMY.ENEMYID, " \
          "ENEMY.CurrentHP " \
          "FROM ITEMTYPE INNER JOIN ITEM ON ITEM.ITEMTYPEID = ITEMTYPE.ITEMTYPEID INNER JOIN " \
          "ENEMYTYPE ON ENEMYTYPE.ENEMYTYPEID = ITEM.ENEMYTYPEID INNER JOIN ENEMY ON " \
          "ENEMY.ENEMYTYPEID = ENEMYTYPE.ENEMYTYPEID WHERE ITEMTYPE.ISARMOR = 1 GROUP BY ENEMY.ENEMYID;"
    cur.execute(sql);
    list = cur.fetchall();
    for str_item in list:
        addstr = str_item[0]
        maxhp = str_item[1]
        maxstr = str_item[2]
        maxhp = maxhp + (20 * addstr)
        maxstr = maxstr + addstr
        cur = db.cursor();
        sql = "UPDATE ENEMYTYPE" \
              " SET ENEMYTYPE.MaxHP = '" + str(maxhp) + "' WHERE ENEMYTYPE.ENEMYTYPEID = '" + str(str_item[3]) + "';"
        cur.execute(sql);
        sql = "UPDATE ENEMYTYPE" \
              " SET ENEMYTYPE.MaxStr = '" + str(maxstr) + "' WHERE ENEMYTYPE.ENEMYTYPEID = '" + str(str_item[3]) + "';"
        cur.execute(sql);
        sql = "UPDATE ENEMY" \
              " SET ENEMY.CurrentHP = '" + str(maxhp) + "' WHERE ENEMY.ENEMYID = '" + str(str_item[4]) + "';"
        cur.execute(sql);
        sql = "UPDATE ENEMY" \
              " SET ENEMY.CurrentStr = '" + str(maxstr) + "' WHERE ENEMY.ENEMYID = '" + str(str_item[4]) + "';"
        cur.execute(sql);
    return


# Format players into starting condition
def format_players():
    cur = db.cursor();
    sql = "SELECT ITEMTYPE.ADDSTR, PLAYERCHARACTER.MAXHP, PLAYERCHARACTER.MAXSTR, PLAYERCHARACTER.PlayerId, " \
          "PLAYERCHARACTER.CurrentHP FROM ITEMTYPE INNER JOIN ITEM ON ITEM.ITEMTYPEID = ITEMTYPE.ITEMTYPEID " \
          "INNER JOIN PLAYERCHARACTER ON PLAYERCHARACTER.PLAYERID = ITEM.PLAYERID WHERE ITEMTYPE.ISARMOR = 1 " \
          "GROUP BY PLAYERCHARACTER.PlayerId;"
    cur.execute(sql);
    list = cur.fetchall();
    for str_item in list:
        addstr = str_item[0]
        maxhp = str_item[1]
        maxstr = str_item[2]
        maxhp = maxhp + (20 * addstr)
        maxstr = maxstr + addstr
        cur = db.cursor();
        sql = "UPDATE PLAYERCHARACTER" \
              " SET PLAYERCHARACTER.MaxHP = '" + str(maxhp) + "' WHERE PLAYERCHARACTER.PlayerId = '" + str(
            str_item[3]) + "';"
        cur.execute(sql);
        sql = "UPDATE PLAYERCHARACTER" \
              " SET PLAYERCHARACTER.MaxStr = '" + str(maxstr) + "' WHERE PLAYERCHARACTER.PlayerId = '" + str(
            str_item[3]) + "';"
        cur.execute(sql);
        sql = "UPDATE PLAYERCHARACTER" \
              " SET PLAYERCHARACTER.CurrentHP = '" + str(maxhp) + "' WHERE PLAYERCHARACTER.PlayerId = '" + str(
            str_item[3]) + "';"
        cur.execute(sql);
        sql = "UPDATE PLAYERCHARACTER" \
              " SET PLAYERCHARACTER.CurrentStr = '" + str(maxstr) + "' WHERE PLAYERCHARACTER.PlayerId = '" + str(
            str_item[3]) + "';"
        cur.execute(sql);
    return


# Format after combat
def format_players_after_combat(loc):
    cur = db.cursor();
    sql = "SELECT PLAYERCHARACTER.MAXHP, PLAYERCHARACTER.MAXSTR, PLAYERCHARACTER.PlayerId, " \
          "PLAYERCHARACTER.CurrentHP FROM PLAYERCHARACTER WHERE PLAYERCHARACTER.LOCATIONID = '" + str(
        loc) + "' GROUP BY PLAYERCHARACTER.PlayerId;"
    cur.execute(sql);
    list = cur.fetchall();
    for p_stat in list:
        maxhp = p_stat[0]
        maxstr = p_stat[1]
        cur = db.cursor();
        sql = "UPDATE PLAYERCHARACTER" \
              " SET PLAYERCHARACTER.MaxHP = '" + str(maxhp) + "' WHERE PLAYERCHARACTER.PlayerId = '" + str(
            p_stat[2]) + "';"
        cur.execute(sql);
        sql = "UPDATE PLAYERCHARACTER" \
              " SET PLAYERCHARACTER.MaxStr = '" + str(maxstr) + "' WHERE PLAYERCHARACTER.PlayerId = '" + str(
            p_stat[2]) + "';"
        cur.execute(sql);
        sql = "UPDATE PLAYERCHARACTER" \
              " SET PLAYERCHARACTER.CurrentHP = '" + str(maxhp) + "' WHERE PLAYERCHARACTER.PlayerId = '" + str(
            p_stat[2]) + "';"
        cur.execute(sql);
        sql = "UPDATE PLAYERCHARACTER" \
              " SET PLAYERCHARACTER.CurrentStr = '" + str(maxstr) + "' WHERE PLAYERCHARACTER.PlayerId = '" + str(
            p_stat[2]) + "';"
        cur.execute(sql);
    return


def enemy_scan(loc):
    i = int(0)
    cur = db.cursor();
    sql = "SELECT ENEMYTYPE.EnemyTypeName, ENEMY.CURRENTHP, ENEMYTYPE.MaxHP, ENEMYTYPE.MaxStr, " \
          " ENEMYTYPE.MaxPerc, ENEMYTYPE.MaxIntel, ENEMYTYPE.MaxLuck " \
          " FROM ENEMYTYPE INNER JOIN ENEMY ON ENEMY.EnemyTypeId = ENEMYTYPE.EnemyTypeId " \
          " WHERE ENEMY.LocationId = '" + loc + "' GROUP BY ENEMY.ENEMYID;"
    cur.execute(sql);
    enemylist = cur.fetchall();
    if len(enemylist) > 0:
        print("\nThe following enemies are in the room:\n")
        for e in enemylist:
            if e[1] > 0:
                ewl = get_weapon_stats_by_user(str(e[0]))
                eal = get_armor_by_user(str(e[0]))
                if eal is None:
                    ea = "No armor"
                else:
                    ea = str(eal[2])
                print(str(e[0]) + str(" | HP: ") + str(int(e[1])) + str(" / ") + str(int(e[2])) + " | " + str(ea)
                      + " | " + str(ewl[3]) + str("\nStrength: ") + str(e[3]) + " | " + str("Perception: ")
                      + str(e[4]) + " | " + str("Intelligence: ") + str(e[5]) + " | " + str("Luck: ")
                      + str(e[6]) + "\n")
            else:
                print(str(e[0]) + str(" (dead)\n"))
    else:
        print("There doesn't seem to be any aliens around.\n")
    return


# Output number of alive players in current location
def get_player_count_in_loc(loc):
    cur = db.cursor();
    sql = "SELECT COUNT(*) FROM PLAYERCHARACTER WHERE PLAYERCHARACTER.LOCATIONID = '" + loc + "' AND PLAYERCHARACTER.CURRENTHP > 0;"
    cur.execute(sql)
    playercount = cur.fetchall();
    for p in playercount:
        playercount = p[0]
    return playercount


# Output number of alive enemies in current location
def get_enemy_count_in_loc(loc):
    cur = db.cursor();
    sql = "SELECT COUNT(*) FROM ENEMY WHERE ENEMY.LOCATIONID = '" + loc + "' AND ENEMY.CURRENTHP > 0;"
    cur.execute(sql)
    enemycount = cur.fetchall();
    for e in enemycount:
        enemycount = e[0]
    return enemycount


# Get player statistics
def get_player_stats(comp):
    companionstats = "No companion"
    cur = db.cursor();
    sql = "SELECT PLAYERCHARACTER.PLAYERID, PLAYERCHARACTER.PLAYERNAME, " \
          "PLAYERCHARACTER.CURRENTHP, PLAYERCHARACTER.MAXHP, " \
          "PLAYERCHARACTER.CURRENTSTR, PLAYERCHARACTER.MAXSTR, " \
          "PLAYERCHARACTER.CURRENTPERC, PLAYERCHARACTER.MAXPERC, " \
          "PLAYERCHARACTER.CURRENTINTEL, PLAYERCHARACTER.MAXINTEL, " \
          "PLAYERCHARACTER.CURRENTLUCK, PLAYERCHARACTER.CURRENTLUCK" \
          " FROM PLAYERCHARACTER" \
          " WHERE PLAYERCHARACTER.PLAYERID = '1' OR PLAYERCHARACTER.PLAYERID = '" + comp + "';"
    cur.execute(sql)
    playerstats = cur.fetchone();
    if playerstats[2] <= 0:
        playerstats = str(playerstats[1]) + " is dead or unconscious."
    if comp != "0":
        companionstats = cur.fetchone();
        if companionstats[2] <= 0:
            companionstats = str(companionstats[1]) + " is dead or unconscious."

    return playerstats, companionstats


def get_all_player_stats_by_playerid(playerid):
    cur = db.cursor();
    sql = "SELECT PLAYERCHARACTER.PLAYERID, PLAYERCHARACTER.PLAYERNAME, " \
          "PLAYERCHARACTER.CURRENTHP, PLAYERCHARACTER.MAXHP, " \
          "PLAYERCHARACTER.CURRENTSTR, PLAYERCHARACTER.MAXSTR, " \
          "PLAYERCHARACTER.CURRENTPERC, PLAYERCHARACTER.MAXPERC, " \
          "PLAYERCHARACTER.CURRENTINTEL, PLAYERCHARACTER.MAXINTEL, " \
          "PLAYERCHARACTER.CURRENTLUCK, PLAYERCHARACTER.CURRENTLUCK" \
          " FROM PLAYERCHARACTER" \
          " WHERE PLAYERCHARACTER.PlayerId = '" + str(playerid) + "';"
    cur.execute(sql)
    p_statlist = cur.fetchall();
    if cur.rowcount >= 1:
        for stat in p_statlist:
            p_id = stat[0]
            p_name = stat[1]
            p_c_hp = stat[2]
            p_m_hp = stat[3]
            p_c_str = stat[4]
            p_m_str = stat[5]
            p_c_perc = stat[6]
            p_m_perc = stat[7]
            p_c_intel = stat[8]
            p_m_intel = stat[9]
            p_c_luck = stat[10]
            p_m_luck = stat[11]
    else:
        print("Something went wrong with player stats fetch.")
        return
    return p_id, p_name, p_c_hp, p_m_hp, p_c_str, p_m_str, p_c_perc, p_m_perc, p_c_intel, p_m_intel, p_c_luck, p_m_luck


def print_playerstats(comp, combat):
    p = int(0)
    if comp != "0" and combat is False:
        players = [1, comp]
    elif comp == "0" and combat is False:
        players = [1]
    elif combat is True:
        players = [comp]
    while p < len(players):
        playerid = players[p]
        sl = get_all_player_stats_by_playerid(playerid)
        if sl[2] <= 0:
            print(str(sl[1]) + " is dead or unconcious!")
            p = p + 1
        else:
            al = get_armor_by_user(str(sl[1]))
            wl = get_weapon_stats_by_user(str(sl[1]))
            print("\n" + str(sl[1]) + " | HP: " + str(int(sl[2])) + " / " + str(int(sl[3])) + " | " + str(al[2]) + " | " + str(wl[3]))
            print("Strength: " + str(sl[4]) + " | Perception: " + str(sl[6]) + " | Intelligence: " + str(sl[8]) + " | Luck: " + str(sl[10]) + " | ")
            p = p + 1
    return


def simple_stats_print(comp):
    print_playerstats(comp, False)
    return


# Output next player name in location; Turn -variable used in combat
def get_next_alive_player_in_loc(loc, turn):
    next_p = ""
    rowcounter = 0
    cur = db.cursor();
    sql = "SELECT PLAYERCHARACTER.PLAYERNAME FROM PLAYERCHARACTER" \
          " WHERE PLAYERCHARACTER.CURRENTHP > 0 AND PLAYERCHARACTER.LOCATIONID = '" + loc + "' GROUP BY PLAYERCHARACTER.PLAYERID ASC;"
    cur.execute(sql)
    rowcount = cur.rowcount

    if rowcount >= 1:
        while rowcounter != turn:
            next_p = None
            next_p = cur.fetchone();
            rowcounter = rowcounter + 1
    else:
        print("Something went wrong!")

    next_playername = next_p[0]
    return next_playername


def get_next_alive_playerid_in_loc(loc, turn):
    next_p_id = ""
    rowcounter = 0
    cur = db.cursor();
    sql = "SELECT PLAYERCHARACTER.PLAYERID FROM PLAYERCHARACTER" \
          " WHERE PLAYERCHARACTER.CURRENTHP > 0 AND PLAYERCHARACTER.LOCATIONID = '" + loc + "' GROUP BY PLAYERCHARACTER.PLAYERID ASC;"
    cur.execute(sql)
    rowcount = cur.rowcount

    if rowcount >= 1:
        while rowcounter != turn:
            next_p_id = None
            next_p_id = cur.fetchone();
            rowcounter = rowcounter + 1
    else:
        print("Something went wrong!")
        return

    next_playerid = next_p_id[0]
    return next_playerid


# Output next enemy name in location; Turn -variable used in combat
def get_next_alive_enemy_in_loc(loc, turn):
    next_e = ""
    rowcounter = 0
    cur = db.cursor();
    sql = "SELECT ENEMYTYPE.ENEMYTYPENAME" \
          " FROM ENEMYTYPE" \
          " INNER JOIN ENEMY ON ENEMY.ENEMYTYPEID = ENEMYTYPE.ENEMYTYPEID" \
          " INNER JOIN LOCATION ON LOCATION.LOCATIONID = ENEMY.LOCATIONID" \
          " WHERE ENEMY.CURRENTHP > 0 AND ENEMY.LOCATIONID = '" + loc + "' GROUP BY ENEMY.ENEMYID DESC;"
    cur.execute(sql)
    rowcount = cur.rowcount

    if rowcount >= 1:
        while rowcounter != turn:
            next_e = None
            next_e = cur.fetchone();
            rowcounter = rowcounter + 1
    else:
        print("Something went wrong!")

    next_enemyname = next_e[0]
    return next_enemyname


def get_next_alive_enemyid_in_loc(loc, turn):
    next_e_id = ""
    rowcounter = 0
    cur = db.cursor();
    sql = "SELECT ENEMY.ENEMYID" \
          " FROM ENEMY" \
          " INNER JOIN LOCATION ON LOCATION.LOCATIONID = ENEMY.LOCATIONID" \
          " WHERE ENEMY.CURRENTHP > 0 AND ENEMY.LOCATIONID = '" + loc + "' GROUP BY ENEMY.ENEMYID DESC;"
    cur.execute(sql)
    rowcount = cur.rowcount

    if rowcount >= 1:
        while rowcounter != turn:
            next_e_id = None
            next_e_id = cur.fetchone();
            rowcounter = rowcounter + 1
    else:
        print("Something went wrong!")

    next_enemyid = next_e_id[0]
    return next_enemyid


# Output list of weapon-stats using username -string
def get_weapon_stats_by_user(username):
    cur = db.cursor();
    sql = "SELECT ITEMTYPE.ITEMTYPEID, ITEMTYPE.ITEMTYPENAME, ITEMTYPE.MINDMG, ITEMTYPE.MAXDMG, " \
          "ITEM.PLAYERID, PLAYERCHARACTER.PLAYERNAME, ITEM.ENEMYTYPEID, ENEMYTYPE.ENEMYTYPENAME" \
          " FROM ITEMTYPE INNER JOIN ITEM ON ITEM.ITEMTYPEID = ITEMTYPE.ITEMTYPEID" \
          " LEFT JOIN PLAYERCHARACTER ON PLAYERCHARACTER.WEAPON = ITEM.ITEMID" \
          " LEFT JOIN ENEMYTYPE ON ENEMYTYPE.ENEMYTYPEID = ITEM.ENEMYTYPEID" \
          " WHERE PLAYERCHARACTER.PLAYERNAME = '" + str(username) + "' OR ENEMYTYPE.ENEMYTYPENAME = '" + str(
        username) + "' AND ITEMTYPE.ISWEAPON = 1;"
    cur.execute(sql);
    weaponstats = cur.fetchall();
    for w in weaponstats:
        w_typeid = w[0]
        w_typename = w[1]
        mindmg = w[2]
        maxdmg = w[3]
        p_ownerid = w[4]
        p_ownername = w[5]
        e_ownertypeid = w[6]
        e_ownername = w[7]
    return mindmg, maxdmg, w_typeid, w_typename, p_ownerid, p_ownername, e_ownertypeid, e_ownername


# Calculate player accuracy
def get_acc_by_player(player_id):
    cur_perc = int()
    cur_luck = int()
    cur = db.cursor();
    sql = "SELECT PLAYERCHARACTER.CURRENTPERC, PLAYERCHARACTER.CURRENTLUCK" \
          " FROM PLAYERCHARACTER WHERE PLAYERCHARACTER.PLAYERID = '" + player_id + "' ;"
    cur.execute(sql)
    p_perceptionstats = cur.fetchall();
    for p in p_perceptionstats:
        cur_perc = p[0]
        cur_luck = p[1]
    p_accuracy = (0.33 + (cur_perc * 0.042) + (cur_luck * 0.0125))
    p_accuracy = round(p_accuracy, 5)
    return p_accuracy


# Calculate enemy accuracy
def get_acc_by_enemy(enemy_id):
    cur_perc = int()
    cur_luck = int()
    cur = db.cursor();
    sql = "SELECT ENEMY.CURRENTPERC, ENEMY.CURRENTLUCK" \
          " FROM ENEMY WHERE ENEMY.ENEMYID = '" + enemy_id + "' ;"
    cur.execute(sql)
    e_perc_luck_stats = cur.fetchall();
    for e in e_perc_luck_stats:
        cur_perc = e[0]
        cur_luck = e[1]
    e_accuracy = (0.33 + (cur_perc * 0.042) + (cur_luck * 0.0125))
    e_accuracy = round(e_accuracy, 5)
    return e_accuracy


# Calculate hit or miss
def calculate_hit_by_accuracy(user_accuracy):
    hit_or_miss = int(0)  # If 1; Hit
    randomfloat = random.uniform(0, 1)
    randomfloat = round(randomfloat, 5)
    # print("uacc:", user_accuracy)
    # print("rndfloat:", randomfloat)
    if user_accuracy >= randomfloat:
        hit_or_miss = 1
    else:
        hit_or_miss = 0
    return hit_or_miss


def get_crit_or_not_by_playerid(player_id):
    p_crit = int(0)
    cur = db.cursor();
    sql = "SELECT CurrentLuck FROM PLAYERCHARACTER WHERE PlayerId = '" + str(player_id) + "';"
    cur.execute(sql)
    p_luck_stats = cur.fetchall();
    for pls in p_luck_stats:
        p_luck = pls[0]
    p_crit_chance = (0.1 + (0.025 * p_luck))
    randomfloat = random.uniform(0, 1)
    # print("pcrit:", p_crit_chance)
    # print("rndfloat:", randomfloat)
    if p_crit_chance >= randomfloat:
        p_crit = int(1)
    else:
        p_crit = int(0)
    return p_crit


def get_crit_or_not_by_enemyid(enemy_id):
    e_crit = int(0)
    cur = db.cursor();
    sql = "SELECT CurrentLuck FROM ENEMY WHERE EnemyId = '" + str(enemy_id) + "';"
    cur.execute(sql)
    e_luck_stats = cur.fetchall();
    for els in e_luck_stats:
        e_luck = els[0]
    e_crit_chance = (0.1 + (0.025 * e_luck))
    randomfloat = random.uniform(0, 1)
    # print("ecrit:", e_crit_chance)
    # print("rndfloat:", randomfloat)
    if e_crit_chance >= randomfloat:
        e_crit = int(1)
    else:
        e_crit = int(0)
    return e_crit


def get_player_dodge_chance_by_id(player_id):
    cur = db.cursor();
    sql = "SELECT CurrentIntel, CurrentLuck FROM PLAYERCHARACTER WHERE PlayerId = '" + str(player_id) + "';"
    cur.execute(sql)
    p_intel_luck_stats = cur.fetchall();
    for pis in p_intel_luck_stats:
        p_intelligence = pis[0]
        p_luck = pis[1]
    p_dodge_chance = (0.1 + (0.01 * p_intelligence) + (0.005 * p_luck))
    return p_dodge_chance


def get_enemy_dodge_chance_by_id(enemy_id):
    cur = db.cursor();
    sql = "SELECT CurrentIntel, CurrentLuck FROM ENEMY WHERE EnemyId = '" + str(enemy_id) + "';"
    cur.execute(sql)
    e_intel_luck_stats = cur.fetchall();
    for eis in e_intel_luck_stats:
        e_intelligence = eis[0]
        e_luck = eis[1]
    e_dodge_chance = (0.1 + (0.01 * e_intelligence) + (0.005 * e_luck))
    return e_dodge_chance


def calculate_dodge_by_dodge_chance(user_dodge_chance):
    dodge_or_not = int(0)
    randomfloat = random.uniform(0, 1)
    randomfloat = round(randomfloat, 5)
    # print("u_ddg_chance:", user_dodge_chance)
    # print("rndfloat:", randomfloat)
    if user_dodge_chance >= randomfloat:
        dodge_or_not = 1
    else:
        dodge_or_not = 0
    return dodge_or_not


# Output random damage using minimum and maximum damage of a weapon
def get_dmg_from_weapon(mindmg, maxdmg):
    base_random_dmg = random.randint(mindmg, maxdmg)
    return base_random_dmg


# Output list of armor-stats using username -string
def get_armor_by_user(username):
    armorid = ""
    armor_typeid = ""
    armor_name = str("No armor.")
    armor_dmg_reduction = int(1)
    e_ownerid = ""
    e_ownername = ""
    p_ownerid = ""
    p_ownername = ""
    cur = db.cursor();
    sql = "SELECT ITEM.ITEMID, ITEMTYPE.ITEMTYPEID, ITEMTYPE.ITEMTYPENAME, ITEMTYPE.DMGREDUCTION, ENEMY.ENEMYID, " \
          "ENEMYTYPE.ENEMYTYPENAME, PLAYERCHARACTER.PLAYERID, PLAYERCHARACTER.PLAYERNAME" \
          " FROM ITEM INNER JOIN ITEMTYPE ON ITEMTYPE.ITEMTYPEID = ITEM.ITEMTYPEID" \
          " LEFT JOIN ENEMY ON ENEMY.ENEMYTYPEID = ITEM.ENEMYTYPEID" \
          " LEFT JOIN ENEMYTYPE ON ENEMYTYPE.ENEMYTYPEID = ENEMY.ENEMYTYPEID" \
          " LEFT JOIN PLAYERCHARACTER ON PLAYERCHARACTER.ARMOR = ITEM.ITEMID" \
          " WHERE ITEMTYPE.ISARMOR = 1 AND PLAYERCHARACTER.PLAYERNAME = '" + username + "' OR ITEMTYPE.ISARMOR = 1 AND ENEMYTYPE.ENEMYTYPENAME = '" + username + "' GROUP BY ITEM.ITEMID;"
    cur.execute(sql)
    armorlist = cur.fetchall();
    if cur.rowcount >= 1:
        for a in armorlist:
            armorid = a[0]
            armor_typeid = a[1]
            armor_name = a[2]
            armor_dmg_reduction = a[3]
            e_ownerid = a[4]
            e_ownername = a[5]
            p_ownerid = a[6]
            p_ownername = a[7]
    elif cur.rowcount == 0:
        return
    else:
        print("Something wrong in getting the armor by username.")

    return armorid, armor_typeid, armor_name, armor_dmg_reduction, e_ownerid, e_ownername, p_ownerid, p_ownername


# Calculate damage reduction from input damage using the armor's damage reduction coefficient
def get_dmg_reduction_by_armor(armor_dmg_reduction, input_dmg):
    d_r_multiplier = armor_dmg_reduction
    i_dmg = input_dmg
    if d_r_multiplier >= 0 and i_dmg >= 0:
        output_dmg = d_r_multiplier * i_dmg
    elif d_r_multiplier is None:
        output_dmg = i_dmg
    else:
        print("Damage reduction error!")
    return output_dmg


# Apply damage to enemy-character
def apply_dmg_to_e(base_random_damage, target):
    cur = db.cursor();
    sql = "SELECT CURRENTHP FROM ENEMY WHERE ENEMYID = '" + str(target) + "';"
    cur.execute(sql);
    curhp = cur.fetchall();
    for chp in curhp:
        curhp = chp[0]
        newhp = curhp - base_random_damage
        cur = db.cursor();
        sql = "UPDATE ENEMYTYPE, ENEMY, ITEMTYPE, ITEM SET ENEMY.CurrentHP = '" + str(
            newhp) + "' WHERE ENEMY.ENEMYID = '" + str(target) + "';"
        cur.execute(sql);
    return


# Apply damage to player-character
def apply_dmg_to_p(base_random_damage, target):
    cur = db.cursor();
    sql = "SELECT CURRENTHP FROM PLAYERCHARACTER WHERE PLAYERID = '" + str(target) + "';"
    cur.execute(sql);
    curhp = cur.fetchall();
    for chp in curhp:
        curhp = chp[0]
        newhp = curhp - base_random_damage
        cur = db.cursor();
        sql = "UPDATE PLAYERCHARACTER, ITEMTYPE, ITEM SET PLAYERCHARACTER.CurrentHP = '" + str(
            newhp) + "' WHERE PLAYERCHARACTER.PLAYERID = '" + str(target) + "';"
        cur.execute(sql);
    return


def surprise_trigger(loc, turn):
    double_dmg = False
    cur = db.cursor();
    sql = "SELECT SURPRISETRIGGER FROM LOCATION WHERE LOCATIONID = '" + str(loc) + "';"
    cur.execute(sql);
    trigger_value = cur.fetchall();
    if cur.rowcount != 1:
        print("Error in surprise trigger. (1)")
        return
    if cur.rowcount == 1:
        for t in trigger_value:
            t_value = t[0]
        if t_value == 0:
            double_dmg = False
            return
        elif t_value == 1:
            double_dmg = True
            cur = db.cursor();
            sql = "UPDATE LOCATION SET SurpriseTrigger = '" + str("0") + "' WHERE LocationId = '" + str(loc) + "';"
            cur.execute(sql);
            return double_dmg
        elif t_value == 2:
            double_dmg = False
            turn = turn + 1
            cur = db.cursor();
            sql = "UPDATE LOCATION SET SurpriseTrigger = '" + str("0") + "' WHERE LocationId = '" + str(loc) + "';"
            cur.execute(sql);
            return turn
        else:
            double_dmg = False
            print("Error in surprise trigger. (3)")
            return
    return


def get_list_of_usables():
    cur = db.cursor();
    sql = "SELECT ITEMTYPE.ITEMTYPENAME, COUNT(*) FROM ITEMTYPE " \
          " INNER JOIN ITEM ON ITEM.ITEMTYPEID = ITEMTYPE.ITEMTYPEID " \
          " INNER JOIN PLAYERCHARACTER ON PLAYERCHARACTER.PLAYERID = ITEM.PLAYERID " \
          " WHERE ITEMTYPE.ISUSABLE = 1 AND ITEM.CURRENTUSENO > 0 AND ITEM.PLAYERID IS NOT NULL " \
          " GROUP BY ITEMTYPE.ITEMTYPENAME;"
    cur.execute(sql);
    if cur.rowcount == 0:
        print("Nothing you can use in combat was found in your inventory.")
        return
    else:
        print("Usable items in combat:")
        usables = cur.fetchall()
        for u in usables:
            print(" - " + str(u[0]) + "(" + str(u[1]) + "x)")
        print("")
        return usables


def use_explosive(loc, turn, target):
    p_username = get_next_alive_player_in_loc(loc, turn)  # Get PlayerName whose turn it is
    cur = db.cursor();
    sql = "SELECT ITEMTYPE.MINDMG, ITEMTYPE.MAXDMG, ITEMTYPE.ITEMTYPENAME, ITEM.ITEMID " \
          " FROM ITEMTYPE " \
          " INNER JOIN ITEM ON ITEM.ITEMTYPEID = ITEMTYPE.ITEMTYPEID " \
          " INNER JOIN PLAYERCHARACTER ON PLAYERCHARACTER.PLAYERID = ITEM.PLAYERID " \
          " WHERE ITEMTYPE.ITEMTYPENAME LIKE '%" + target + "%' AND ITEMTYPE.ISUSABLE = 1 AND " \
                                                            " ITEM.CURRENTUSENO > 0 AND ITEM.PLAYERID IS NOT NULL GROUP BY ITEMTYPE.ITEMTYPENAME;"
    cur.execute(sql);
    if cur.rowcount == 0:
        print("No such usable found.")
        turn = turn
        return turn
    elif cur.rowcount > 1:
        print("Please be more specific.")
        turn = turn
        return turn
    elif cur.rowcount == 1:
        item = cur.fetchall();
        for i in item:
            exp_min_dmg = i[0]
            exp_max_dmg = i[1]
            exp_name = i[2]
            exp_id = i[3]
        exp_dmg = random.randint(exp_min_dmg, exp_max_dmg)
        cur = db.cursor();
        sql = "SELECT ENEMYID, CURRENTHP FROM ENEMY WHERE LOCATIONID = '" + str(loc) + "' AND CURRENTHP > 0 ;"
        cur.execute(sql);
        cur = db.cursor();
        sql = "UPDATE ENEMY SET CURRENTHP = CURRENTHP - '" + str(exp_dmg) + "' WHERE LOCATIONID = '" + str(loc) + "';"
        cur.execute(sql)
        sql = "UPDATE ITEM SET PLAYERID = NULL, CURRENTUSENO = CURRENTUSENO - '" + str(1) + "' WHERE ITEMID = '" + str(
            exp_id) + "';"
        cur.execute(sql)
        print(str(p_username) + " throws " + str(exp_name) + " at the enemy. The explosion causes " + str(
            exp_dmg) + " points of internal damage to all aliens in the room.")
        turn = turn + 1
        return turn


# Attack -function used by players
def attack(loc, target):
    attacked_enemy = ""
    target_id = ""
    target_typename = ""
    e_hp = ""
    if target == str("first enemy"):
        turn = get_enemy_count_in_loc(loc)
        target = get_next_alive_enemy_in_loc(loc, turn)
    else:
        target = target
    cur = db.cursor();
    sql = "SELECT ENEMY.ENEMYID, ENEMY.ENEMYTYPEID, ENEMYTYPE.ENEMYTYPENAME, ENEMY.CURRENTHP" \
          " FROM ENEMY INNER JOIN ENEMYTYPE ON ENEMYTYPE.ENEMYTYPEID = ENEMY.ENEMYTYPEID" \
          " WHERE ENEMY.CURRENTHP > 0 AND ENEMY.LOCATIONID = '" + loc + "' AND ENEMYTYPE.ENEMYTYPENAME = '" + target + "'GROUP BY ENEMY.CURRENTHP;"
    cur.execute(sql)
    if cur.rowcount >= 1:
        invalid_target = 0
        enemy = cur.fetchone();
        attacked_enemy = enemy[2]
        target_id = enemy[0]
        target_typename = enemy[1]
        e_hp = enemy[3]
    elif cur.rowcount < 1:
        invalid_target = 1
    return attacked_enemy, target_id, target_typename, e_hp, invalid_target


# Attack -function used by enemies
def enemy_attack(loc, comp):
    attacked_player = ""
    p_targetid = ""
    p_hp = int(0)
    while p_hp <= 0:
        enemy_target = ""
        enemy_target = enemy_target_selector(comp)
        cur = db.cursor();
        sql = "SELECT PLAYERID, PLAYERNAME, CURRENTHP FROM PLAYERCHARACTER WHERE CURRENTHP > 0 AND " \
              " LOCATIONID = '" + str(loc) + "' AND PLAYERID = '" + str(enemy_target) + "' GROUP BY CURRENTHP;"
        cur.execute(sql)
        if cur.rowcount >= 1:
            player = cur.fetchone();
            attacked_player = player[1]
            p_targetid = player[0]
            p_hp = player[2]
    return attacked_player, p_targetid, p_hp


def enemy_target_selector(comp):
    if comp != "0":
        r = [1, comp]
        enemy_target = random.choice(r)
        return enemy_target
    else:
        enemy_target = 1
        return enemy_target

      
def levelup(comp):
    cur = db.cursor();
    sql = "UPDATE PLAYERCHARACTER SET MAXHP = MAXHP + '" + str(20) + "' where playerid = '1' or playerid = '" + str(comp) + "' ;"
    cur.execute(sql);
    return
      

# Main combat loop
def combat(loc, comp):
    previous_command = ""
    loc = loc
    print("\n----------------------------------------------------------------------\n"
          "PREPARE FOR COMBAT!"
          "\n----------------------------------------------------------------------\n")

    print_playerstats(comp, False)
    enemy_scan(loc)

    while get_player_count_in_loc(loc) != 0 and get_enemy_count_in_loc(loc) != 0:

        p_max_turns = (get_player_count_in_loc(loc))  # PLAYER'S COMBAT TURN STARTS
        turn = int(1)  # Format turn -counter

        st_value = surprise_trigger(loc, turn)  # Surprise trigger
        if st_value == 2:  # Enemy gets the first turn
            print("The enemy attacks from out of nowhere! Get to cover!")
            while turn <= p_max_turns:
                turn = st_value
                turn = turn + 1
        elif st_value is True:  # 2x to all damage on first player turn, except explosive + guaranteed hit
            myprint("The enemy hasn't noticed you. You should probably use this to "
                    "your advantage and get a few easy shots into them.")

        while turn <= p_max_turns and get_enemy_count_in_loc(loc) > 0:  # PLAYER'S COMBAT LOOP STARTS

            p_id = get_next_alive_playerid_in_loc(loc, turn)  # Get player id
            p_name = get_next_alive_player_in_loc(loc, turn)

            print("")
            input_string = input(str(p_name) + "'s combat action? ");  # Player input start

            # Quality of life improvements below:
            if input_string == "attack":
                input_string = "attack first enemy"
                previous_command = input_string
            elif input_string == str("p"):
                input_string = previous_command
            elif input_string != str("p"):
                previous_command = input_string

            action, target = ParseInput(input_string);

            if action == "attack":

                attacked_enemy = attack(loc, target)  # Get list of data for target enemy
                target_enemy_id = attacked_enemy[1]  # Target enemy id
                targetname_enemy = attacked_enemy[0]  # Name of target enemy
                e_invalid_choice = attacked_enemy[4]  # If 0: Should be valid target, ie. exist in location / not dead

                if e_invalid_choice == 1:  # Valid target or not
                    print("\nNo such enemy is alive! Try again!\n")
                else:
                    p_username = get_next_alive_player_in_loc(loc, turn)  # Get PlayerName whose turn it is
                    p_id = str(get_next_alive_playerid_in_loc(loc, turn))  # Get PlayerId whose turn it is

                    p_accuracy = get_acc_by_player(p_id)  # Get PlayerId accuracy
                    p_hit_miss = calculate_hit_by_accuracy(p_accuracy)  # Calculate hit or miss
                    if p_hit_miss == 0 and st_value is not True:
                        turn = turn + 1
                        print(str(p_username) + " attacks the " + str(attacked_enemy[0]) + " and misses!")

                    else:
                        p_weaponstats = get_weapon_stats_by_user(p_username)  # Get data for player's current weapon
                        p_w_mindmg = p_weaponstats[0]
                        p_w_maxdmg = p_weaponstats[1]

                        p_rnd_dmg = get_dmg_from_weapon(p_w_mindmg, p_w_maxdmg)  # Random damage creation

                        p_crit = get_crit_or_not_by_playerid(p_id)
                        if p_crit == 1 and st_value is True:  # Quadruple damage
                            p_rnd_dmg = (2 * (p_rnd_dmg * 2))
                            print("The enemy doesn't even know what hit 'em!")
                        elif p_crit == 1 and st_value is not True:  # Normal critical hit
                            p_rnd_dmg = (p_rnd_dmg * 2)
                            # print("Critical hit!")
                        elif p_crit == 0 and st_value is True:  # Double damage from surprise trigger
                            p_rnd_dmg = (p_rnd_dmg * 2)
                            print("Surprise attack!")
                        elif p_crit == 0 and st_value is not True:  # Normal damage
                            p_rnd_dmg = p_rnd_dmg
                        else:
                            print("Something wrong in crit calc")  # Debug

                        e_dodge_chance = get_enemy_dodge_chance_by_id(target_enemy_id)
                        e_dodge_or_not = calculate_dodge_by_dodge_chance(e_dodge_chance)
                        if e_dodge_or_not == 1 and p_crit == 1 and st_value is not True:  # Dodge critical hit
                            turn = turn + 1
                            myprint("The " + str(targetname_enemy) + " almost gets hit straight in the "
                                    "face, but dodges at the last moment. Buggers!")
                        elif e_dodge_or_not == 1 and p_crit == 0 and st_value is not True:  # Dodge normal hit
                            turn = turn + 1
                            print("The " + str(targetname_enemy) + " barely dodges. Bloody hell these guys are quick!")
                        else:  # Didn't dodge

                            e_armor = get_armor_by_user(
                                targetname_enemy)  # Get list of data for enemy armor, if there's any

                            if e_armor is None:  # If enemy has no armor
                                p_armor_dmg_red_mult = int(1)
                            else:
                                p_armor_dmg_red_mult = e_armor[3]  # Damage reduction coefficient

                            # Final damage done to enemy
                            p_final_dmg = get_dmg_reduction_by_armor(p_armor_dmg_red_mult, p_rnd_dmg)
                            p_final_dmg = round(p_final_dmg)

                            if p_crit != 1:  # Normal hit
                                turn = turn + 1
                                print(str(p_username) + " attacks the " + str(targetname_enemy) + " for " + str(
                                    p_final_dmg) + " points of damage.")
                                apply_dmg_to_e(p_final_dmg, target_enemy_id)  # PLAYER'S COMBAT TURN ENDS
                            elif p_crit == 1:  # Critical hit
                                turn = turn + 1
                                print(str(p_username) + " attacks the " + str(targetname_enemy) + " for a "
                                "critical amount of " + str(p_final_dmg) + " damage points!")
                                apply_dmg_to_e(p_final_dmg, target_enemy_id)  # PLAYER'S COMBAT TURN ENDS
                            elif e_invalid_choice == 1:  # Invalid target, player gets to retry
                                turn = turn
                                print("No such alien is alive.")
                            else:  # In case of error
                                print("Something went wrong with the player combat loop.")

            # Combat usables below
            elif action == "use":
                if "grenade" in target or "charge" in target:
                    turn = use_explosive(loc, turn, target)
                usables = get_list_of_usables()  # List available usables
            else:
                print("\nInvalid command!\n")

        e_max_turns = get_enemy_count_in_loc(loc)  # ENEMY COMBAT TURN STARTS
        turn = int(1)

        if get_enemy_count_in_loc(loc) > 0:  # Making sure there's still enemies around

            print("\nEnemy turn starts")

            while turn <= e_max_turns and get_player_count_in_loc(loc) > 0:  # ENEMY COMBAT LOOP STARTS
                # print("Enemy turn " + str(turn) + ":")

                attacked_player = enemy_attack(loc, comp)
                target_player_id = attacked_player[1]
                targetname_player = attacked_player[0]

                e_username = get_next_alive_enemy_in_loc(loc, turn)
                e_id = str(get_next_alive_enemyid_in_loc(loc, turn))

                e_accuracy = get_acc_by_enemy(e_id)
                e_hit_or_miss = calculate_hit_by_accuracy(e_accuracy)
                if e_hit_or_miss == 0:
                    turn = turn + 1
                    print(str(e_username) + " attacks " + str(attacked_player[0]) + " and misses!")

                else:
                    e_weaponstats = get_weapon_stats_by_user(e_username)
                    e_w_mindmg = e_weaponstats[0]
                    e_w_maxdmg = e_weaponstats[1]

                    e_rnd_dmg = get_dmg_from_weapon(e_w_mindmg, e_w_maxdmg)

                    e_crit = get_crit_or_not_by_enemyid(e_id)
                    if e_crit == 1:
                        e_rnd_dmg = (e_rnd_dmg * 2)
                    elif e_crit == 0:
                        e_rnd_dmg = e_rnd_dmg
                    else:
                        print("Something wrong in crit calc")

                    p_dodge_chance = get_player_dodge_chance_by_id(target_player_id)
                    p_dodge_or_not = calculate_dodge_by_dodge_chance(p_dodge_chance)
                    if p_dodge_or_not == 1 and e_crit == 1:
                        turn = turn + 1
                        myprint("HAH! " + str(targetname_player) + " barely dodges the attack heading straight"
                                " for the head! That really could've hurt otyherwise...")
                    elif p_dodge_or_not == 1 and e_crit == 0:
                        turn = turn + 1
                        print("Pfft... " + str(targetname_player) + " dodges the attack with ease.")
                    else:

                        p_armor = get_armor_by_user(targetname_player)  # Get list of data for player armor
                        if p_armor is None:
                            p_armor_dmg_red_mult = int(1)
                        else:
                            p_armor_dmg_red_mult = p_armor[3]

                        # Final damage done to player
                        e_final_dmg = get_dmg_reduction_by_armor(p_armor_dmg_red_mult, e_rnd_dmg)
                        e_final_dmg = round(e_final_dmg)

                        if targetname_player is not None and e_crit != 1:
                            turn = turn + 1
                            print(str(e_username) + " attacks " + str(targetname_player) + " for " + str(
                                e_final_dmg) + " points of damage.")
                            apply_dmg_to_p(e_final_dmg, target_player_id)
                        elif targetname_player is not None and e_crit == 1:
                            turn = turn + 1
                            print(str(e_username) + " attacks " + str(
                                targetname_player) + " for a critical amount of " + str(
                                e_final_dmg) + " damage points.")
                            apply_dmg_to_p(e_final_dmg, target_player_id)
                        else:
                            print("Something wrong with enemy combat loop.")
                            break  # Just in case
            print_playerstats(comp, False)
            enemy_scan(loc)
        # else: ↓↓↓↓↓ Continue to Combat ending ↓↓↓↓↓
    # COMBAT ENDS | COMBAT ENDS | COMBAT ENDS | COMBAT ENDS | COMBAT ENDS |
    if get_enemy_count_in_loc(loc) == 0:  # Game continues
        print("\n----------------------------------------------------------------------\n")
        print("All the pesky enemies are dead! RIP in peace.\n")
        levelup(comp)
        format_players_after_combat(loc)  # Formats players to pre-combat
        done = int(0)

    elif get_player_count_in_loc(loc) == 0:  # LOOSING CONDITION | GAME OVER |
        print("You're dead and the Earth is doomed!")
        print("\n----------------------------------------------------------------------\n"
              "GAME OVER!"
              "\n----------------------------------------------------------------------\n")
        done = str("GAME OVER")

    return done


# Custom print
def myprint(text):
    row_l = 70
    l = text.split()
    used = 0
    for word in l:
        if used + len(word) <= row_l:
            if used > 0:
                print(" ", end='')
                used = used + 1
            print(word, end='')
        else:
            print('')
            used = 0
            print(word, end='')
        used = used + len(word)
    print('')


# HELP
def showHelp():
    cur = db.cursor();
    sql = "SELECT textblock FROM storycontainer WHERE storyid = 0;";
    cur.execute(sql);
    h = cur.fetchall();

    print(h[0][0]);


# PARSER
def ParseInput(str):
    # seperates action and target and returns them
    # ONLY SUPPORTS TWO PARAMETERS! (action and target)

    # Possible actions! ADD YOUR OWN!
    actions = ["move", "pick up", "hack", "inventory", "equip", "use", "attack", "look", "examine", "help"];
    action = "";
    target = "";

    # Loops through actions list.
    # If matches with input string sets action
    for a in actions:
        if str.startswith(a):
            action = a;
    # Sets target by deleting action from input string
    target = str.replace(action + " ", "");

    return action, target;


# START OF THE GAME || START OF THE GAME || START OF THE GAME || START OF THE GAME || START OF THE GAME ||


format_enemies()  # Format all enemies

format_players()  # Format all players

done = int(0)  # Format end -condition to 0
loc = "105"  # Starting location
comp = '0'  # Companion variable
turn = 1  # Format turn, mostly for debug

story(loc, comp)
show_location(loc)
show_passages(loc)
showDropped(loc);

# MAIN LOOP STARTS HERE || MAIN LOOP STARTS HERE || MAIN LOOP STARTS HERE || MAIN LOOP STARTS HERE ||


while done == 0:

    print("")
    input_string = input("Your action? ");
    action, target = ParseInput(input_string);
    print("")

    # ADD ACTIONS HERE! MAKE SURE THEY MATCH actions[] in ParseInput()
    # pick up
    if action == "pick up":
        pickItem(loc, target);
    # move
    elif action == "move":
        loc = move(loc, target, comp)
        # if all players died in combat
        if loc == str("GAME OVER"):
            done = 1
    # hack
    elif action == "hack":
        hacking(loc, target)
    # show inventory
    elif action == "inventory":
        showInv(comp);
    # help
    elif action == "help":
        showHelp();
    elif action == "equip":
        equipItem(target, comp);
    # use
    elif action == "use":
        if loc == "103" and 'keycard' in target and comp == '0':
            comp = use_jailcellkeycard(loc, target)
            story(loc, comp)
            show_passages(loc)
        elif loc == '115' and 'pod' in target:
            loc = use_icepod(loc, target, comp)
            story(loc, comp)
            show_location(loc)
            enemy_scan(loc)
            show_passages(loc)
            showDropped(loc);
        elif loc == '213' and 'keycard' in target:
            use_elevatorkeycard(loc, target)
        elif loc == '205' and 'keycard' in target:
            use_egckeycard(loc, target)
        elif loc == '206' and 'cd' in target:
            done = use_cd(loc, target, comp)
        elif loc == '208' and 'console' in target:
            use_powersupply(loc, target, comp)
        elif loc == '215' and 'telecom' in target:
            use_telecom(loc, target, comp)
        else:
            print("You can't use that!")
    # look/examine
    elif action == "look":
        if target == "room":
            show_location(loc)
            enemy_scan(loc)
            show_passages(loc)
            showDropped(loc);
    elif action == "examine":
        examine(loc, target, comp);
    else:
        print("Invalid command!");

    # print("Parsed action: " + action)
    # print("Parsed target: " + target)
    print("")

db.close()
