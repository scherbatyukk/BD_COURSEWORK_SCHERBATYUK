from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config

Base = declarative_base()
engine = create_engine(f'postgresql://{Config.user}:{Config.passwd}@{Config.url}/{Config.db_name}')
session = sessionmaker(bind=engine)()


def recreate_database():
    print('Recreating database...')
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def defineGenerateStringFunc():
    session.execute('create or replace function generateString(length int) '
                   'returns text '
                   'language plpgsql '
                   'as '
                   '$$ '
                   'declare '
                   'outputString text; '
                   'begin '
                   'select string_agg(chr(trunc(97 + random()*25)::int), \'\') '
                   'from generate_series(1, length) '
                   'into outputString; '
                   'return outputString; '
                   'end; '
                   '$$; ')
    session.commit()


def defineGenerateDateFunc():
    session.execute('create function generatedate() returns date '
                   'language plpgsql '
                   'as '
                   '$$ '
                   'declare '
                   'outputDate date; '
                   'begin '
                   'select date (timestamp \'2000-01-01\' + random() * (timestamp \'2020-12-31\' - timestamp \'2000-01-01\')) '
                   'into outputDate; '
                   'return outputDate; '
                   'end; '
                   '$$; ')
    session.commit()


def defineGenerateIntFunc():
    session.execute('create function generateint(max integer) returns text '
                   'language plpgsql '
                   'as '
                   '$$ '
                   'declare '
                   'outputInt int; '
                   'begin '
                   'select trunc(random() * max + 1) '
                   'into outputInt; '
                   'return outputInt; '
                   'end; '
                   '$$; ')
    session.commit()


def defineGetRandowRowFunc():
    session.execute('create or replace function getrandomrow(table_name text) returns text '
                   'language plpgsql '
                   'as '
                   '$$ '
                   'declare '
                   'output int; '
                   'begin '
                   'EXECUTE format(\'select id from "%s" ORDER BY random() LIMIT 1\', table_name) '
                   'into output; '
                   'return output; '
                   'end; '
                   '$$; ')
    session.commit()


def initCustomFunctions():
    defineGenerateStringFunc()
    defineGenerateDateFunc()
    defineGenerateIntFunc()
    defineGetRandowRowFunc()