## Get all RADIUS users:

`https://<controler_ip>/proxy/network/v2/api/site/<site>/radius/users`

`<site>` is normally "default" or the name of another site if you hav one.i

## Get all OS users:

`https://<controler_ip>/proxy/users/api/v2/users/search`

With filters: `https://<controler_ip>/proxy/users/api/v2/users/search?including_resource=true&page_num=1&page_size=25&condition=&expand=with_last_activity,with_assignments&group_id=`

## Get all OS user groups:

`https://<controler_ip>/proxy/users/api/v2/user_groups`