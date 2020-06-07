drop schema public cascade;
create schema public;


CREATE OR REPLACE FUNCTION Create_tables() returns void as $$
    begin
        create table if not exists first_table
    (
        name character varying,
        id integer not null generated always as identity,
        amount integer,
        total integer,
        primary key (id)
    );create index if not exists name on first_table (name);

    create table if not exists second_table
    (
        id integer not null generated always as identity,
        person character varying,
        satisfaction character varying,
        creation_time timestamptz default CURRENT_TIMESTAMP,
        update_time timestamptz,
        primary key (id)
    );
    end
 $$ language plpgsql;


select Create_tables();


create or replace function add_items_to_first_table  (_name character varying, _amount integer, _total integer) returns void as $$
    begin
        insert into first_table (name, amount, total) values (_name, _amount, _total);
    end
$$ language plpgsql;



create or replace function set_update_time()
returns trigger as 
$$
begin 
	NEW.update_time = CURRENT_TIMESTAMP;
	return NEW;
end;
$$ language plpgsql;


drop trigger if exists update_second_time on second_table;
create trigger update_second_time before update
	on second_table for each row execute procedure
	set_update_time();


create or replace function add_items_to_second_table (_person character varying, _satisfaction character varying) returns void as $$
    begin
        insert into second_table (person, satisfaction) values (_person, _satisfaction);
    end
$$ language plpgsql;


drop function if exists get_data_from_first_table ();

create or replace function get_data_from_first_table()
returns  table (name character varying
		, id integer
		, amount integer
		, total integer)as
$$
begin
    return query
    select * from first_table;
end
$$ language plpgsql;


drop function if exists get_data_from_second_table();
create or replace function get_data_from_second_table()
returns table (id integer
		  , person character varying
		  , satisfaction character varying
		  , creation_time timestamptz
		  , update_time timestamptz)as
$$
begin
    return query
    select * from second_table;
end
$$ language plpgsql;
    


create or replace function delete_from_first_table(target int)
returns void as
$$
begin
    delete from second_table where id = target;
    delete from first_table where id = target;
end
$$ language plpgsql;


create or replace function delete_from_second_table (target int) returns void as
$$
begin
    delete from second_table where id = target;
end
$$ language plpgsql;


drop function if exists show_active_databases ();

create or replace function show_active_databases () returns setof name as
$$
begin
	return query (select datname from pg_database);
end
$$ language plpgsql;


drop function if exists find_in_first_table_integer ();

create or replace function find_in_first_table_integer(target integer) 
returns table (name character varying
		, id integer
		, amount integer
		, total integer)as
$$
begin
	return query (
	select * from first_table 
	where     target = first_table.amount	
	or   target = first_table.total);
end
$$ language plpgsql;



drop function if exists find_in_first_table_character ();

create or replace function find_in_first_table_character(target character varying) 
returns table (name character varying
		, id integer
		, amount integer
		, total integer)as
$$
begin
	return query(
	select * from first_table 
	where  target::text 
	 like concat('%',first_table.name::text,'%'));
end
$$ language plpgsql;


drop function if exists find_in_second_table_character ();

create or replace function find_in_second_table_character(target text ) 
returns table (id integer
		, person character varying
		, satisfaction character varying
		, creation_time timestamptz
		, update_time timestamptz) as
$$
begin
	return query(
	select * from second_table 
	where  target::text 
	like concat('%',second_table.person::text,'%')::text 
	or target::text 
	like concat('%', second_table.satisfaction::text,'%')::text );
end
$$ language plpgsql;




drop function if exists  delete_all_in_tables();
create or replace function delete_all_in_tables()
returns void as
$$
begin
	truncate first_table;
	truncate second_table;
end
$$ language plpgsql;



drop function if exists  delete_all_in_first_table();
create or replace function delete_all_in_first_table()
returns void as
$$
begin
	truncate first_table;
end
$$ language plpgsql;


drop function if exists  delete_all_in_second_table();
create or replace function delete_all_in_second_table()
returns void as
$$
begin
	truncate second_table;
end
$$ language plpgsql;




drop function if exists  update_name_in_first_table();
create or replace function update_name_in_first_table(old_id integer, new_name character varying)
returns void as
$$
begin
	update first_table 
	set name = new_name
	where first_table.id = old_id;
end
$$ language plpgsql;



drop function if exists  update_amount_in_first_table();
create or replace function update_amount_in_first_table(old_id integer, new_amount integer)
returns void as
$$
begin
	update first_table 
	set amount = new_amount
	where first_table.id = old_id;
end
$$ language plpgsql;




drop function if exists  update_total_in_first_table();
create or replace function update_total_in_first_table(old_id integer, new_total integer)
returns void as
$$
begin
	update first_table 
	set total = new_total
	where first_table.id = old_id;
end
$$ language plpgsql;



drop function if exists  update_person_in_second_table();
create or replace function update_person_in_second_table(old_id integer, new_person character varying)
returns void as
$$
begin
	update second_table 
	set person = new_person
	where second_table.id = old_id;
end
$$ language plpgsql;


drop function if exists  update_satisfaction_in_second_table();
create or replace function update_satisfaction_in_second_table(old_id integer, new_satisfaction character varying)
returns void as
$$
begin
	update second_table 
	set satisfaction = new_satisfaction
	where second_table.id = old_id;
end
$$ language plpgsql;


