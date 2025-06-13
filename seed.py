from datetime import datetime

from app import create_app
from models import db
from models import (
    Area, SpecialLocation,
    BaitCategory, Bait, Rod, Look, Fruit,
    DecorationCategory, Decoration, DecorationItem, Homeplan, HomeFish,
    Fish, AreaFish, FishdexNotepad, CaughtTime, CaughtDate, CollectionCompletion,
    FishingLine, FishingLog,
    ChatLog, PM,
    Club, ClubPlayer, ClubFish,
    NPC, Config, ConfigNPC,
    Payment,
    OutfitTemplate, Outfit,
    Item, ShopItem,
    Player, PlayerSettings, PlayerStats, MoneyTree, AreaRegistration, UpgradeRecord,
    MoneyHistory,
    Penalty, Reject, ReportRecord,
    Task, TaskAward, TaskCompletion,
    Trade
)
from enums.enum_inventory_type import InventoryType
from enums.enum_registration_type import RegistrationType
from enums.enum_rod_sizes import RodSizes
from enums.enum_width_unit import WidthUnit
from enums.enum_penalty_type import PenaltyType
from enums.enum_report_status import ReportStatus
from enums.enum_upgrade_type import UpgradeType


def seed_db():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        area = Area(name='Test Area', badge_id=1, area_id=1, level_requirement=1).create()
        sub_area = Area(name='Sub Area', badge_id=2, area_id=2, level_requirement=1, parent_area=area).create()
        SpecialLocation(name='Cave', title='The Cave', area=area).create()

        bait_cat = BaitCategory(name='Basic Baits').create()
        bait = Bait(name='Worm', bait_id=1, category=bait_cat).create()
        rod = Rod(name='Starter Rod', size=RodSizes.Normal, length_quality=1).create()
        look = Look(name='Casual').create()
        fruit = Fruit(name='Apple').create()

        decoration_cat = DecorationCategory(name='Default', description='Default category').create()
        decoration = Decoration(name='Chair', homepoints=10, category=decoration_cat).create()
        homeplan = Homeplan().create()
        DecorationItem(x=0, y=0, floor=0, homeplan=homeplan, decoration=decoration).create()

        fish = Fish(name='Salmon').create()
        AreaFish(area=area, fish=fish).create()
        FishdexNotepad(player=None, fish=fish).create()
        CaughtTime(time_range='Morning', fish=fish).create()
        CaughtDate(date_range='Spring', fish=fish).create()
        CollectionCompletion(completion_id=1, fish=fish).create()

        player = Player(username='john', email='john@example.com', password_hash='hash').create()
        PlayerSettings(player=player, width_unit=WidthUnit.feet).create()
        PlayerStats(player=player, total_game_play_hours=0).create()
        MoneyTree(player=player, level=1).create()
        FishingLine(player=player, level=1, color='red').create()

        bait_item = Item(amount=5, item_type=InventoryType.Bait, bait=bait, player=player).create()
        rod_item = Item(amount=1, item_type=InventoryType.Rod, rod=rod, player=player).create()
        Item(amount=1, item_type=InventoryType.Look, look=look, player=player).create()
        Item(amount=2, item_type=InventoryType.Fruit, fruit=fruit, player=player).create()
        Item(amount=1, item_type=InventoryType.Decoration, decoration=decoration, player=player).create()
        ShopItem(amount=1, item_type=InventoryType.Bait, bait=bait).create()

        # Set player's currently selected bait and rod
        player.current_bait_item = bait_item
        player.current_rod_item = rod_item
        player.commit()

        Payment(created_date=datetime.utcnow(), owner='owner', amount=0.0, status='pending').create()

        npc = NPC(name='Guide').create()
        Config(raft_start_time=datetime.utcnow(), raft_end_time=datetime.utcnow()).create()
        ConfigNPC(herb_amount=1, vasily_rate=1, herb_area=area, herb_fish=fish).create()

        outfit_template = OutfitTemplate(player=player, title='Default Template', style='casual').create()
        Outfit(sex=1, skin_color='white', outfit_template=outfit_template).create()

        HomeFish(is_completed=False, fish=fish, player=player).create()

        ChatLog(username='john', message='Hello', created_date=datetime.utcnow()).create()
        PM(subject='Hi', content='Welcome', receiver=player, sender=player, created_date=datetime.utcnow()).create()

        club = Club(name='My Club', leader=player, created_date=datetime.utcnow()).create()
        ClubPlayer(club=club, player=player, created_date=datetime.utcnow()).create()
        ClubFish(club=club, fish=fish).create()

        MoneyHistory(is_fish_bucks=True, amount=100, description='Initial', player=player, created_date=datetime.utcnow()).create()

        Penalty(penalty_type=PenaltyType.PM, period_minutes=10, moderator=player, penalized_player=player, created_date=datetime.utcnow()).create()
        Reject(description='spam', moderator=player).create()
        ReportRecord(report_type='Abuse', title='Spam', description='Spam message', status=ReportStatus.Pending, reported_player=player, reporting_by_player=player, reviewer_moderator=player, created_date=datetime.utcnow()).create()

        trade = Trade(traded_with_npc=False, area=area, given_by=player, taken_by=player, created_date=datetime.utcnow()).create()
        Item(amount=1, item_type=InventoryType.Fruit, fruit=fruit, trade_given=trade, player=player).create()
        Item(amount=1, item_type=InventoryType.Rod, rod=rod, trade_taken=trade, player=player).create()

        task = Task(name='Sample Task', description='Catch fish', fishing_mission_quantity=1, is_shine_fishing_log=False, star_rate=1, fish_length=10, area_registration_type=RegistrationType.TroutFarm, area=area, fish=fish, npc=npc).create()
        TaskAward(amount=1, item_type=InventoryType.Fishcoins, task=task).create()
        TaskCompletion(completed=False, catched_fish_amount=0, task=task, player=player).create()
        UpgradeRecord(upgrade_type=UpgradeType.FishingLine, player=player, created_date=datetime.utcnow()).create()
        AreaRegistration(registration_type=RegistrationType.HarborBoat, duration_seconds=3600, player=player, created_date=datetime.utcnow()).create()

        FishingLog(fish=fish, area=area, bait=bait, player=player, rod=rod, is_shiny=False, earned_xp=10.0, width=5.5, created_date=datetime.utcnow()).create()

        db.session.commit()

if __name__ == '__main__':
    seed_db()
