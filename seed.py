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
from enums.enum_record_status import RecordStatus
from enums.enum_upgrade_type import UpgradeType


def seed_db():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        area = Area(name='Test Area', badge_id=1, area_id=1, level_requirement=1).create(commit=False)
        sub_area = Area(name='Sub Area', badge_id=2, area_id=2, level_requirement=1, parent_area=area).create(commit=False)
        SpecialLocation(name='Cave', title='The Cave', area=area).create(commit=False)

        bait_cat = BaitCategory(name='Basic Baits').create(commit=False)
        bait = Bait(name='Worm', bait_id=1, category=bait_cat).create(commit=False)
        rod = Rod(name='Starter Rod', size=RodSizes.Normal, length_quality=1).create(commit=False)
        look = Look(name='Casual').create(commit=False)
        fruit = Fruit(name='Apple').create(commit=False)

        decoration_cat = DecorationCategory().create(commit=False)
        decoration = Decoration(name='Chair', homepoints=10, category=decoration_cat).create(commit=False)
        homeplan = Homeplan().create(commit=False)
        DecorationItem(x=0, y=0, floor=0, homeplan=homeplan, decoration=decoration).create(commit=False)

        fish = Fish(name='Salmon').create(commit=False)
        AreaFish(area=area, fish=fish).create(commit=False)
        FishdexNotepad(player=None, fish=fish).create(commit=False)
        CaughtTime(time_range='Morning', fish=fish).create(commit=False)
        CaughtDate(date_range='Spring', fish=fish).create(commit=False)
        CollectionCompletion(completion_id=1, fish=fish).create(commit=False)

        player = Player(username='john', email='john@example.com', password_hash='hash').create(commit=False)
        PlayerSettings(player=player, width_unit=WidthUnit.feet).create(commit=False)
        PlayerStats(player=player, total_game_play_hours=0).create(commit=False)
        MoneyTree(player=player, level=1).create(commit=False)
        FishingLine(player=player, level=1, color='red').create(commit=False)

        Item(amount=5, item_type=InventoryType.Bait, bait=bait, player=player).create(commit=False)
        Item(amount=1, item_type=InventoryType.Rod, rod=rod, player=player).create(commit=False)
        Item(amount=1, item_type=InventoryType.Look, look=look, player=player).create(commit=False)
        Item(amount=2, item_type=InventoryType.Fruit, fruit=fruit, player=player).create(commit=False)
        Item(amount=1, item_type=InventoryType.Decoration, decoration=decoration, player=player).create(commit=False)
        ShopItem(amount=1, item_type=InventoryType.Bait, bait=bait).create(commit=False)

        Payment(created_date=datetime.utcnow(), owner='owner').create(commit=False)

        npc = NPC(name='Guide').create(commit=False)
        Config(raft_start_time=datetime.utcnow(), raft_end_time=datetime.utcnow()).create(commit=False)
        ConfigNPC(herb_amount=1, vasily_rate=1, herb_area=area, herb_fish=fish).create(commit=False)

        outfit_template = OutfitTemplate(player=player).create(commit=False)
        Outfit(sex=1, skin_color='white', outfit_template=outfit_template).create(commit=False)

        HomeFish(is_completed=False, fish=fish, player=player).create(commit=False)

        ChatLog(username='john', message='Hello', created_date=datetime.utcnow()).create(commit=False)
        PM(subject='Hi', content='Welcome', receiver=player, sender=player, created_date=datetime.utcnow()).create(commit=False)

        club = Club(leader=player, created_date=datetime.utcnow()).create(commit=False)
        ClubPlayer(club=club, player=player, created_date=datetime.utcnow()).create(commit=False)
        ClubFish(club=club, fish=fish).create(commit=False)

        MoneyHistory(is_fish_bucks=True, amount=100, description='Initial', player=player, created_date=datetime.utcnow()).create(commit=False)

        Penalty(penalty_type=PenaltyType.PM, period_minutes=10, moderator=player, penalized_player=player, created_date=datetime.utcnow()).create(commit=False)
        Reject(description='spam', moderator=player).create(commit=False)
        ReportRecord(report_type='Abuse', title='Spam', description='Spam message', status=RecordStatus.Pending, reported_player=player, reporting_by_player=player, reviewer_moderator=player, created_date=datetime.utcnow()).create(commit=False)

        trade = Trade(traded_with_npc=False, area=area, given_by=player, taken_by=player, created_date=datetime.utcnow()).create(commit=False)
        Item(amount=1, item_type=InventoryType.Fruit, fruit=fruit, trade_given=trade, player=player).create(commit=False)
        Item(amount=1, item_type=InventoryType.Rod, rod=rod, trade_taken=trade, player=player).create(commit=False)

        task = Task(fishing_mission_quantity=1, is_shine_fishing_log=False, star_rate=1, fish_length=10, area_registration_type=RegistrationType.TroutFarm, area=area, fish=fish, npc=npc).create(commit=False)
        TaskAward(amount=1, item_type=InventoryType.Fishcoins, task=task).create(commit=False)
        TaskCompletion(completed=False, catched_fish_amount=0, task=task, player=player).create(commit=False)
        UpgradeRecord(upgrade_type=UpgradeType.FishingLine, player=player, created_date=datetime.utcnow()).create(commit=False)
        AreaRegistration(registration_type=RegistrationType.HarborBoat, duration_seconds=3600, player=player, created_date=datetime.utcnow()).create(commit=False)

        FishingLog(fish=fish, area=area, bait=bait, player=player, rod=rod, is_shiny=False, earned_xp=10.0, width=5.5, created_date=datetime.utcnow()).create(commit=False)

        db.session.commit()

if __name__ == '__main__':
    seed_db()
